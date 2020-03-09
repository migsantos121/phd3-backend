from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """

"""

response_body = """
{
    "action_summary": {
        "bookmark_summary": {
            "positive": 0
        }, 
        "is_bookmarked": false, 
        "is_shared": false, 
        "is_liked": false, 
        "is_disliked": false, 
        "share_summary": {
            "positive": 0
        }, 
        "comments_count": 0, 
        "like_summary": {
            "positive": 0, 
            "negative": 0
        }
    }
}
"""

test_case = {
    "request": {
        "path_params": {"article_id": "1"},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["read"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01GetArticleAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetArticleAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase01GetArticleAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)

    def setupOAuth(self, scopes):
        super(TestCase01GetArticleAPITestCase, self).setupOAuth(scopes)

        from django.contrib.auth import get_user_model
        user_model = get_user_model()
        user = user_model.objects.create(username='admin', is_staff=True)

        conn = {
            "user": user,
            "access_token": self.foo_access_token
        }

        request_data = {
            "published_time": "2017-04-12 12:21",
            "title": "This is new",
            "url": "string",
            "author_name": "string",
            "summary": "string",
            "tags": ""
        }





