from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "notification_type": "string", 
    "sort_by_date": "ASC", 
    "limit": 1, 
    "offset": 1, 
    "source": "string"
}
"""

response_body = """
{
    "total_count": 1, 
    "unread_count": 1, 
    "notifications": [
        {
            "notification_id": 1, 
            "read_at": "string", 
            "creation_datetime": "string", 
            "service": "string", 
            "title": "string", 
            "read_status": true, 
            "cm_token": "string", 
            "notification_type": "string", 
            "message": "string", 
            "extra_data": "string"
        }
    ]
}
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


class TestCase01GetUserNotificationsAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetUserNotificationsAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase01GetUserNotificationsAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


