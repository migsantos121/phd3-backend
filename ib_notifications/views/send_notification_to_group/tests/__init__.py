# Endpoint Configuration

APP_NAME = "ib_notifications"
OPERATION_NAME = "send_notification_to_group"
REQUEST_METHOD = "post"
URL_SUFFIX = "notifications/send_group_notification/"


from .test_case_01 import TestCase01SendNotificationToGroupAPITestCase

__all__ = [
    "TestCase01SendNotificationToGroupAPITestCase"
]


