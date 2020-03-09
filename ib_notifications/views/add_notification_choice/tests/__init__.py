# Endpoint Configuration

APP_NAME = "ib_notifications"
OPERATION_NAME = "add_notification_choice"
REQUEST_METHOD = "post"
URL_SUFFIX = "notifications/add_notification_choice/"


from .test_case_01 import TestCase01AddNotificationChoiceAPITestCase

__all__ = [
    "TestCase01AddNotificationChoiceAPITestCase"
]


