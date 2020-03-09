from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "content": "This is test content", 
    "article_id": 1,
    "multimedia_type": "",
    "multimedia_url": ""
}
"""

response_body = """
{"post_id": 1}
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


class TestCase01AddPostAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01AddPostAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase01AddPostAPITestCase, self).test_case()
        self.assertEqual(response.status_code, 200)

    def setupUser(self, username, password):
        super(TestCase01AddPostAPITestCase, self).setupUser(username, password)

        self.foo_user.first_name = "user"
        self.foo_user.save()


