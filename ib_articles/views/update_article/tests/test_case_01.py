from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

request_body = """
{
    "title": "new title", 
    "url": "url", 
    "summary": "summary"
}
"""

response_body = """

"""

test_case = {
    "request": {
        "path_params": {"article_id": "1"},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["write"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password",
                                 "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01UpdateArticleAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01UpdateArticleAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX,
                                                                 test_case,
                                                                 *args, **kwargs)

    def test_case(self):
        from ib_articles.models import Article, ArticleVernacularDetails
        article = Article.objects.create(_title="a", _summary="s", _url="u", _published_time="2012-08-12 12:21",
                      _author_name='t')

        ArticleVernacularDetails.objects.create(article=article, v_title="a", v_summary="s", v_url="u", v_published_time="2012-08-12 12:21",
                               v_author_name='t')

        response = super(TestCase01UpdateArticleAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)

    def setupUser(self, username, password):
        super(TestCase01UpdateArticleAPITestCase, self).setupUser(username, password)

        self.foo_user.first_name = "user"
        self.foo_user.is_staff=True
        self.foo_user.save()
