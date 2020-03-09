from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
[
    {
        "keyword": "keyword1",
         "group_id": 1
    }, 
    {
        "keyword": "keyword2",
        "group_id": 1
    }
]
"""

response_body = """
{"res_status": "One of keyword group not exist", "response": {}, "http_status_code": 417}
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
        "status": 417,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01AddKeywordsAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01AddKeywordsAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase01AddKeywordsAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 417)


