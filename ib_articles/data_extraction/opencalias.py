import json

import requests

from ib_articles.models import KeywordGroup, Keyword, ArticleKeywordMap, KeywordVernacularDetails


def get_calais_response_dict(article_data):
    """

    :param article_data:
    :return:
    """
    calais_url = 'https://api.thomsonreuters.com/permid/calais'
    access_token = "asqcBXuavMnhar2FeMCRxRhnLcGFqZhM"

    article_xml_data = """
    <Document><Source></Source><Body>{0}</Body></Document>
    """.format(article_data)
    headers = {'X-AG-Access-Token': access_token, 'Content-Type': 'text/xml', 'outputformat': 'application/json',
               'Accept': 'application/json'}
    response = requests.post(calais_url, data=article_xml_data, headers=headers, timeout=80)
    content = response.text
    # return content
    return json.loads(content)


def add_keywords_to_db(article_id, calais_response_dict, keyword_group_list):
    """

    :param article_id:
    :param calais_response_dict:
    :return:
    """

    article_keyword_map_list = []
    for each_key, val in calais_response_dict.items():
        keyword = val.get("name", '').encode('utf-8')
        keyword_group = val.get("_typeGroup", '').encode('utf-8')
        keyword_sub_group = val.get("_type", '').encode('utf-8')

        if val.get("_typeGroup") == "socialTag" and val.get("_typeGroup") not in ["relations"]:
            relevance = (100 - 33 * (int(val.get("importance")) - 1)) / 100.0
        elif val.get("_typeGroup") == "topics":
            relevance = val.get("score", 0)
        else:
            relevance = val.get("relevance", 0)
        if keyword is not '':
            keyword_group_id, keyword_group_list = get_keyword_group_id(keyword_group_list, keyword_group,
                                                                        keyword_sub_group)

            keyword_obj, created = Keyword.objects.get_or_create(
                _keyword=keyword,
                keyword_group_id=keyword_group_id
            )

            keyword_vernacular_obj, created = KeywordVernacularDetails.objects.get_or_create(
                keyword=keyword_obj,
                v_keyword=keyword
            )

            article_keyword_map = ArticleKeywordMap(
                keyword=keyword_obj,
                article_id=article_id,
                relevance=relevance
            )
            article_keyword_map_list.append(article_keyword_map)

    return article_keyword_map_list


def get_keyword_group_id(keyword_group_list, group, sub_group):
    for each_keyword_group in keyword_group_list:
        if each_keyword_group['group'] == group and each_keyword_group['sub_group'] == sub_group:
            return each_keyword_group['id'], keyword_group_list

    from django.conf import settings
    data = {
        "group": group,
        "sub_group": sub_group,
        "group_weight": settings.DEFAULT_GROUP_WEIGHT
    }
    keyword_group_obj = KeywordGroup.objects.create(**data)
    data.update({'id': keyword_group_obj.id})
    keyword_group_list.append(data)
    return keyword_group_obj.id, keyword_group_list


def keywords_from_article_source_tags(article_id, tags, keyword_group_list):
    tags_list = []
    if tags is not None:
        tags_list = tags.split(",")

    article_keyword_map_list = []

    from django.conf import settings
    for each_tag in tags_list:
        keyword_group_id, keyword_group_list = get_keyword_group_id(keyword_group_list, each_tag, '')
        keyword_obj, created = Keyword.objects.get_or_create(
            _keyword=each_tag,
            keyword_group_id=keyword_group_id
        )
        keyword_vernacular_obj, created = KeywordVernacularDetails.objects.get_or_create(
            keyword=keyword_obj,
            v_keyword=each_tag
        )

        article_keyword_map = ArticleKeywordMap(
            keyword=keyword_obj,
            article_id=article_id,
            relevance=settings.DEFAULT_SOURCE_KEYWORDS_RELEVANCE
        )
        article_keyword_map_list.append(article_keyword_map)

    return article_keyword_map_list


def extract_keywords():
    from ib_articles.models import Article
    articles = Article.objects.filter(is_keywords_added=False)

    from ib_common.vernacular_utils.vernacular_utilities_class import VernacularUtilitiesClass
    language_name = VernacularUtilitiesClass.validate_language()[0]

    [article.set_language_specific_attributes(language_name=language_name) for article in articles]
    keyword_group_list = list(KeywordGroup.objects.all().values())
    all_articles_keyword_map_list = []

    for each_article in articles:
        calais_response_dict = get_calais_response_dict(each_article.summary.encode('utf-8', 'ignore'))
        article_keyword_map_list = add_keywords_to_db(each_article.id, calais_response_dict, keyword_group_list)
        all_articles_keyword_map_list.extend(article_keyword_map_list)

        article_keyword_map_list = keywords_from_article_source_tags(each_article.id, each_article.tags,
                                                                     keyword_group_list)
        all_articles_keyword_map_list.extend(article_keyword_map_list)

    ArticleKeywordMap.objects.bulk_create(all_articles_keyword_map_list)
    articles.update(is_keywords_added=True)


if __name__ == "__main__":
    extract_keywords()
