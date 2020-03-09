from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "username": "string", 
    "phone_number": "string", 
    "auth_type": "string", 
    "email": "string", 
    "country_code": "string"
}
"""

response_body = """
[
    {
        "is_staff": true, 
        "first_name": "string", 
        "m_id": 1, 
        "extra_details": [
            {
                "ud_value": "string", 
                "ud_key": "string"
            }
        ], 
        "m_pic": "string", 
        "dob": "2099-12-31 00:00:00", 
        "m_country_code": "string", 
        "m_username": "string", 
        "is_active": true, 
        "is_phone_verified": true, 
        "m_pic_thumbnail": "string", 
        "last_name": "string", 
        "is_admin": true, 
        "is_email_verified": true, 
        "m_status": "string", 
        "m_email": "string", 
        "m_name": "string", 
        "m_phone_number": "string", 
        "m_gender": "string"
    }
]
"""

"""
Write your test case description here
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


class TestCase01SearchUserByAuthTypeAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01SearchUserByAuthTypeAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase01SearchUserByAuthTypeAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


