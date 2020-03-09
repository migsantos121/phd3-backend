from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

request_body = """
{
    "search_q": "", 
    "limit": 10, 
    "filters": {
        "sorts": {
            "published_time": "desc"
        }, 
        "article_ids": [
            1
        ]
    }, 
    "offset": 0
}
"""

response_body = """
[
    {
        "keywords": [], 
        "news_source": null, 
        "published_time": "2012-08-12 12:21:00", 
        "title": "title", 
        "url": "url", 
        "image": null, 
        "tags": "", 
        "author_name": "tanmay", 
        "summary": "summary", 
        "article_id": 1
    }
]
"""

test_case = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["write"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01GetArticleByIdsAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetArticleByIdsAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        from ib_articles.models.article import Article
        a = Article.objects.create(_title="title", _summary="summary", _url="url", _published_time="2012-08-12 12:21:00",
                               _author_name='tanmay', _tags='')
        response = super(TestCase01GetArticleByIdsAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


