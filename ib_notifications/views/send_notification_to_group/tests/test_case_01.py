from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "group_id": 1, 
    "name": "string", 
    "title": "string", 
    "log_notification": true, 
    "source": "string", 
    "notification_type": "string", 
    "message": "string", 
    "extra_data": "string", 
    "cm_type": "string"
}
"""

response_body = """
{"notification_id": 1}
"""

test_case = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["write"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01SendNotificationToGroupAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01SendNotificationToGroupAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase01SendNotificationToGroupAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


