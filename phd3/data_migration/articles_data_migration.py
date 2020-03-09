def get_article_ids_dict(news_source_id_dict, rss_source_id_dict):
    from api.models import Article as APIArticle
    api_articles = APIArticle.objects.all().values()
    articles_list = []
    from ib_articles.models import Article
    for each_api_article in api_articles:
        article_obj = Article(
            _title=each_api_article['title'],
            _url=each_api_article['link'],
            _summary=each_api_article['summary'],
            _author_name=each_api_article['author_name'],
            _published_time=each_api_article['publish_date'],
            _image=each_api_article['image'],
            news_source_id=news_source_id_dict[each_api_article['news_source_id']],
            rss_feed_id=rss_source_id_dict[each_api_article['rss_source_id']]
        )
        articles_list.append(article_obj)
    Article.objects.bulk_create(articles_list)
    article_ids_dict = {}
    article_objects = Article.objects.all().values('id', '_title', '_url')
    for each in api_articles:
        for inner_each in article_objects:
            if inner_each["_title"] == each["title"] and inner_each["_url"] == each["link"]:
                article_ids_dict[each["id"]] = inner_each["id"]
                break
    return article_ids_dict


def map_article_keywords(article_ids_dict, keyword_id_dict):
    from api.models import Article as APIArticle
    api_articles = APIArticle.objects.prefetch_related('keyword').all()

    from ib_articles.models import ArticleKeywordMap
    from django.conf import settings

    for index, each in enumerate(api_articles):
        print index
        article_keyword_map_objects = []
        for inner_index, each_keyword in enumerate(each.keyword.all().values('id', 'name')):
            _obj = ArticleKeywordMap(
                article_id=article_ids_dict[each.id],
                keyword_id=keyword_id_dict[each_keyword["id"]],
                relevance=settings.DEFAULT_SOURCE_KEYWORDS_RELEVANCE
            )
            article_keyword_map_objects.append(_obj)
            print "inner_index", inner_index
        if article_keyword_map_objects:
            try:
                ArticleKeywordMap.objects.bulk_create(article_keyword_map_objects)
            except Exception, err:
                print err


def get_news_source_dict():
    from api.models import NewsSource as APINewsSource
    api_news_sources = APINewsSource.objects.all().values('id', 'name', 'url')
    news_source_list = []
    news_source_id_dict = {}
    from ib_articles.models import NewsSource
    for each in api_news_sources:
        _obj = NewsSource(name=each["name"], url=each["url"])
        news_source_list.append(_obj)
    NewsSource.objects.bulk_create(news_source_list)
    new_news_source_objects = NewsSource.objects.all().values('id', 'name', 'url')
    for each in api_news_sources:
        for inner_each in new_news_source_objects:
            if inner_each["name"] == each["name"] and inner_each["url"] == each["url"]:
                news_source_id_dict[each["id"]] = inner_each["id"]
                break
    return news_source_id_dict


def get_category_dict():
    from api.models import Category as APICategory
    api_categories = APICategory.objects.all().values('id', 'name')
    category_list = []
    category_id_dict = {}
    from ib_articles.models import Category
    for each in api_categories:
        _obj = Category(name=each["name"])
        category_list.append(_obj)
    Category.objects.bulk_create(category_list)
    new_category_objects = Category.objects.all().values('id', 'name')
    for each in api_categories:
        for inner_each in new_category_objects:
            if inner_each["name"] == each["name"]:
                category_id_dict[each["id"]] = inner_each["id"]
                break
    return category_id_dict


def get_keyword_dict():
    from api.models import Keyword_From_Source as APIKeyword
    api_keywords = APIKeyword.objects.all().values('id', 'name')
    keyword_list = []
    keywords = []
    keyword_id_dict = {}
    from ib_articles.models import Keyword
    default_group = Keyword.get_default_group()

    for each in api_keywords:
        if each["name"] not in keywords:
            _obj = Keyword(_keyword=each["name"], keyword_group=default_group)
            keyword_list.append(_obj)
            keywords.append(each["name"])
    Keyword.objects.bulk_create(keyword_list)
    new_keyword_objects = Keyword.objects.all().values('id', '_keyword')
    for each in api_keywords:
        for inner_each in new_keyword_objects:
            if inner_each["_keyword"] == each["name"]:
                keyword_id_dict[each["id"]] = inner_each["id"]
                break
    return keyword_id_dict


def get_rss_source_dict(news_source_id_dict, category_id_dict):
    from api.models import RssSource as APIRssSource
    api_rss_sources = APIRssSource.objects.all().values('id', 'rss_url', 'news_source_id', 'category_id')
    rss_source_list = []
    rss_source_id_dict = {}
    rss_list = []
    from ib_articles.models import RSSFeed
    for each in api_rss_sources:

        rss_str = "%s-%s-%s" % (each["rss_url"],
                                news_source_id_dict[each["news_source_id"]],
                                category_id_dict[each["category_id"]])
        if rss_str not in rss_list:
            _obj = RSSFeed(
                url=each["rss_url"],
                news_source_id=news_source_id_dict[each["news_source_id"]],
                category_id=category_id_dict[each["category_id"]],
            )
            rss_source_list.append(_obj)
            rss_list.append(rss_str)

    RSSFeed.objects.bulk_create(rss_source_list)
    new_rss_source_objects = RSSFeed.objects.all().values('id', 'url', 'news_source_id', 'category_id')
    for each in api_rss_sources:
        for inner_each in new_rss_source_objects:
            if inner_each["url"] == each["rss_url"]:
                rss_source_id_dict[each["id"]] = inner_each["id"]
                break
    return rss_source_id_dict


def migrate_articles():
    print "inserting news source ids"
    news_source_id_dict = get_news_source_dict()
    print "news source len: %d" % len(news_source_id_dict)
    print "inserting category ids"
    category_id_dict = get_category_dict()
    print "inserting category ids done"
    print "inserting rss ids"
    rss_source_id_dict = get_rss_source_dict(news_source_id_dict, category_id_dict)
    print "inserting rss ids done"
    print "inserting keyword ids"
    keyword_id_dict = get_keyword_dict()
    print "inserting keyword ids done"
    print "inserting articles"
    article_ids_dict = get_article_ids_dict(news_source_id_dict, rss_source_id_dict)
    print "inserting articles done"
    print "map articles"
    map_article_keywords(article_ids_dict, keyword_id_dict)
    print "map articles done"
