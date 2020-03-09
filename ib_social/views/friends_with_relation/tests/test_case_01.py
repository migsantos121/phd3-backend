from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "r_m_id": 1, 
    "limit": 1, 
    "relation": "FRIEND", 
    "r_m_type": "string", 
    "offset": 1
}
"""

response_body = """
{"count": 1, "friends": [{"user_id": 1, "user_name": "string", "user_thumbnail": "string"}, {"user_id": 1, "user_name": "string", "user_thumbnail": "string"}]}
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


class TestCase01FriendsWithRelationAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01FriendsWithRelationAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase01FriendsWithRelationAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


