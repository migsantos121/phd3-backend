from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "username": "string", 
    "phone_number": "string", 
    "country_code": "string", 
    "client_id": "string", 
    "client_secret": "string", 
    "email": "string", 
    "auth_type": "string"
}
"""

response_body = """
{"m_id": 1, "m_pic": "string", "dob": "2099-12-31 00:00:00", "m_pic_thumbnail": "string", "m_username": "string", "m_name": "string"}
"""

test_case = {
    "request": {
        "path_params": {},
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


class TestCase01GetUserByAuthTypeAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetUserByAuthTypeAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase01GetUserByAuthTypeAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


