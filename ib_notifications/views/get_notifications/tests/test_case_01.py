from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "source": "source1",
    "limit": 0,
    "offset": 4
}
"""

response_body = """
{
    "notifications": [
        {
            "notification_id": 1,
            "service": "service",
            "title": "title",
            "members_details": [
                {
                    "read_status": false,
                    "device_ids": [
                        "device_id_1",
                        "device_id_2"
                    ],
                    "user_id": "user_id",
                    "read_at": null
                },
                {
                    "read_status": false,
                    "device_ids": [
                        "device_id_1",
                        "device_id_2"
                    ],
                    "user_id": "user_id2",
                    "read_at": null
                }
            ],
            "message": "message",
            "extra_data": "extra_data"
        },
        {
            "notification_id": 2,
            "service": "service2",
            "title": "title2",
            "members_details": [],
            "message": "message2",
            "extra_data": "extra_data2"
        }
    ],
    "total": 2
}
"""

test_case = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["user"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password",
                                 "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01GetNotificationsAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetNotificationsAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD,
                                                                    URL_SUFFIX, test_case,
                                                                    *args, **kwargs)

    def test_case(self):
        from ib_notifications.models.notification import Notification
        notification_1 = Notification.objects.create(service="service",
                                                     title="title",
                                                     source="source1",
                                                     message="message",
                                                     extra_data="extra_data")

        Notification.objects.create(service="service2",
                                    title="title2",
                                    source="source1",
                                    message="message2",
                                    extra_data="extra_data2")

        device_ids = ["device_id_1", "device_id_2"]
        device_ids_string = ",".join(device_ids)
        from ib_notifications.models.notification_receiver import NotificationReceiver
        notification_receiver = NotificationReceiver.objects.create(user_id="user_id",
                                                                    device_ids=device_ids_string
                                                                    )
        notification_receiver2 = NotificationReceiver.objects.create(user_id="user_id2",
                                                                    device_ids=device_ids_string
                                                                    )
        notification_1.members.add(notification_receiver)
        notification_1.members.add(notification_receiver2)
        notification_1.save()

        response = super(TestCase01GetNotificationsAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)
