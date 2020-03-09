from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

request_body = """
{
    "sorts": {
        "posted_date": "string", 
        "published_time": "desc"
    }, 
    "published_time": {
        "start_date_time": "2012-08-12 12:20:00", 
        "end_date_time": "2012-08-12 12:31:00"
    }, 
    "article_ids": [
        1
    ]
}
"""

response_body = """
[
    {
        "published_time": "2012-08-12 12:21:00", 
        "title": "title", 
        "url": "url", 
        "image": null, 
        "tags": null, 
        "author_name": "tanmay", 
        "summary": "summary"
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


class TestCase01GetBasicArticlesAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetBasicArticlesAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD,
                                                                    URL_SUFFIX, test_case,
                                                                    *args, **kwargs)

    def test_case(self):
        from ib_articles.models import Article, ArticleVernacularDetails, NewsSource

        n = NewsSource.objects.create(name='bbc', url='http://bbc.co')
        a = Article.objects.create(_title="title", _summary="summary", _url="url",
                                   _published_time="2012-08-12 12:21:00",
                                   _author_name='tanmay', news_source=n)

        b = ArticleVernacularDetails.objects.create(v_title="title", v_summary="summary", v_url="url",
                                                    v_published_time="2012-08-12 12:21:00",
                                                    v_author_name='tanmay', article=a)

        response = super(TestCase01GetBasicArticlesAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)
