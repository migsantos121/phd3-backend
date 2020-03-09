from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "username": "string", 
    "firstName": "string", 
    "lastName": "string", 
    "userStatus": 1, 
    "phone": "string", 
    "password": "string", 
    "id": 1
}
"""

response_body = """
{"username": "string", "id": 1}
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


class TestCase01CreateUserAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01CreateUserAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase01CreateUserAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


