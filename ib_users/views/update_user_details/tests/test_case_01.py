from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "user_details": [
        {
            "ud_value": "9440357121",
            "ud_key": "phone_number"
        },
        {
            "ud_value": "img.jpg",
            "ud_key": "pic"
        }
    ]
}
"""

response_body = """
{
    "res_status": "200 OK, status=200"
}
"""

test_case = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["read", "write"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01UpdateUserDetailsAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01UpdateUserDetailsAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD,
                                                                     URL_SUFFIX, test_case,
                                                                     *args, **kwargs)

    def test_case(self):
        response = super(TestCase01UpdateUserDetailsAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)

        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(username=self.foo_user.username)
        self.assertEqual(user.pic, 'img.jpg')
        self.assertEqual(user.phone_number, '9440357121')
        self.assertEqual(user.is_phone_verified, False)