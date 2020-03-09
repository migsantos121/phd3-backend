from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "device_types": [
        "string", 
        "string"
    ], 
    "source": "string", 
    "user_id": 1
}
"""

response_body = """

"""

"""
Write your test case description here
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


class TestCase01DeactivateUserAccessTokensApiAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01DeactivateUserAccessTokensApiAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        # response = super(TestCase01DeactivateUserAccessTokensApiAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(200, 200)


