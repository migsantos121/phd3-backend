from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

request_body = """
{
    "search_q": "", 
     "offset":0,
    "filters": {
        "sorts": {
            "published_time":"asc"
        }, 
        "user_ids": [
            1
        ]
    },
    "limit":10
}
"""

response_body = """
[
    {
        "keywords": [], 
        "news_source": {
            "url": "http://bbc.co", 
            "name": "bbc"
        }, 
        "published_time": "2012-08-12 12:21:00", 
        "title": "title", 
        "url": "url", 
        "image": null, 
        "tags": null, 
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


class TestCase01GetArticlesAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetArticlesAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX,
                                                               test_case,
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
        response = super(TestCase01GetArticlesAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)

    def setupUser(self, username, password):
        super(TestCase01GetArticlesAPITestCase, self).setupUser(username, password)

        self.foo_user.first_name = "user"
        self.foo_user.save()
