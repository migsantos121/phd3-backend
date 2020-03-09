"""
Write your test case description here
"""

from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case \
    import CustomAPITestCase


REQUEST_BODY = """
{
    "social_provider_token": "string", 
    "client_secret": "string", 
    "provider": "string", 
    "client_id": "string", 
    "social_provider_token_secret": "string"
}
"""

RESPONSE_BODY = """
{
    "tokens": {
        "access_token": "string", 
        "refresh_token": "string"
    }, 
    "username": "string", 
    "user_id": 1, 
    "res_status": "string"
}
"""

TEST_CASE = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {},
        "body": REQUEST_BODY,
    },
    "response": {
        "status": 200,
        "body": RESPONSE_BODY,
        "header_params": {}
    }
}


class TestCase01TwitterResponseAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
        super(TestCase01TwitterResponseAPITestCase, self). \
            __init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, 
                     TEST_CASE, *args, **kwargs)

    def test_case(self):
        response = super(TestCase01TwitterResponseAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


