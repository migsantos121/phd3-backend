from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

request_body = """
{
    "password": "string1234"
}
"""

response_body = """
"""

test_case = {
    "request": {
        "path_params": {},
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


class TestCase01SetPasswordAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01SetPasswordAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX,
                                                               test_case,
                                                               *args, **kwargs)

    def test_case(self):
        response = super(TestCase01SetPasswordAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)

    def setupUser(self, username, password):
        super(TestCase01SetPasswordAPITestCase, self).setupUser(username, password)

        self.foo_user.first_name = "user"
        self.foo_user.save()
