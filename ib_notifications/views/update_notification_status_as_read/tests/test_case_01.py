from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "notification_id": "1",
    "user_ids": [
        "user_id"
    ]
}
"""

response_body = """

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


class TestCase01UpdateNotificationStatusAsReadAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01UpdateNotificationStatusAsReadAPITestCase, self).__init__(APP_NAME, OPERATION_NAME,
                                                                                  REQUEST_METHOD, URL_SUFFIX, test_case,
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

        user_id = "user_id"
        device_ids = ["device_id_1", "device_id_2"]
        device_ids_string = ",".join(device_ids)
        from ib_notifications.models.notification_receiver import NotificationReceiver
        notification_receiver = NotificationReceiver.objects.create(user_id=user_id,
                                                                    device_ids=device_ids_string
                                                                    )
        notification_1.members.add(notification_receiver)
        notification_1.save()

        response = super(TestCase01UpdateNotificationStatusAsReadAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)

        notification = Notification.objects.get(pk=1)
        notification_receiver = notification.members.get(user_id="user_id")
        self.assertEqual(notification_receiver.read_status, True)
