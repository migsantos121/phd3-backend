from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "entity_id": 1, 
    "entity_type": "string", 
    "limit": 1, 
    "offset": 1
}
"""

response_body = """
{"entity_id": 1, "comments": [{"comment": "string", "username": "string", "user_id": 1, "up_votes": 1, "comment_id": 1, "down_votes": 1, "user_thumbnail_url": "string", "multimedia_url": "string", "multimedia_type": "string"}, {"comment": "string", "username": "string", "user_id": 1, "up_votes": 1, "comment_id": 1, "down_votes": 1, "user_thumbnail_url": "string", "multimedia_url": "string", "multimedia_type": "string"}], "entity_type": "string"}
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


class TestCase01GetCommentsAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetCommentsAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase01GetCommentsAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


