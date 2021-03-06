from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "username": "string", 
    "client_secret": "string", 
    "auth_type": "string", 
    "client_id": "string"
}
"""

response_body = """
{"username": "string", "user_id": 1}
"""

test_case = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01ResendOtpV2APITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01ResendOtpV2APITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase01ResendOtpV2APITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


