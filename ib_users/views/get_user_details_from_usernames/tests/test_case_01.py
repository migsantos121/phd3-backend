from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "usernames": [
        "string", 
        "string"
    ]
}
"""

response_body = """
[{"m_id": 1, "is_admin": "string", "m_pic": "string", "m_status": "string", "dob": "2099-12-31 00:00:00", "m_username": "string", "m_pic_thumbnail": "string", "m_name": "string"}, {"m_id": 1, "is_admin": "string", "m_pic": "string", "m_status": "string", "dob": "2099-12-31 00:00:00", "m_username": "string", "m_pic_thumbnail": "string", "m_name": "string"}]
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


class TestCase01GetUserDetailsFromUsernamesAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetUserDetailsFromUsernamesAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase01GetUserDetailsFromUsernamesAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


