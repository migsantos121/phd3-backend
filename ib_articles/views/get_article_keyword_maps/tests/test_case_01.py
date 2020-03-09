from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "keyword_ids": [
        1
    ]
}
"""

response_body = """
[
    {
        "relevance": 0.91, 
        "keyword_id": 1, 
        "article_id": 1, 
        "keyword_group": {
            "group_weight": 0.1, 
            "sub_group": "sub_group", 
            "group": "group"
        }
    }
]
"""

test_case = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["read"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password",
                                 "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01GetArticleKeywordMapsAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetArticleKeywordMapsAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD,
                                                                         URL_SUFFIX, test_case,
                                                                         *args, **kwargs)

    def test_case(self):
        from ib_articles.models import Article, ArticleVernacularDetails, NewsSource, ArticleKeywordMap, Keyword, \
            KeywordGroup

        n = NewsSource.objects.create(name='bbc', url='http://bbc.co')
        a = Article.objects.create(_title="title", _summary="summary", _url="url",
                                   _published_time="2012-08-12 12:21:00",
                                   _author_name='tanmay', news_source=n)

        b = ArticleVernacularDetails.objects.create(v_title="title", v_summary="summary", v_url="url",
                                                    v_published_time="2012-08-12 12:21:00",
                                                    v_author_name='tanmay', article=a)

        keyword_group = KeywordGroup.objects.create(
            group="group",
            sub_group="sub_group",
            group_weight=0.1
        )
        keyword = Keyword.objects.create(
            _keyword="keyword",
            keyword_group=keyword_group
        )

        ArticleKeywordMap.objects.create(
            keyword=keyword,
            article=a,
            relevance=0.91
        )

        response = super(TestCase01GetArticleKeywordMapsAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)
