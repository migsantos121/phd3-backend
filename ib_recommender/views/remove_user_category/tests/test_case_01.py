from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """

"""

response_body = """
{"res_status": "", "response": "Category Id not found", "http_status_code": 404}
"""

test_case = {
    "request": {
        "path_params": {"category_id": "1234"},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["read"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 404,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01RemoveUserCategoryAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01RemoveUserCategoryAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase01RemoveUserCategoryAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 404)


