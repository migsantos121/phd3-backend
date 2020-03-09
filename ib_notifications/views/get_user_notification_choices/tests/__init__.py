# Endpoint Configuration

APP_NAME = "ib_notifications"
OPERATION_NAME = "get_user_notification_choices"
REQUEST_METHOD = "post"
URL_SUFFIX = "notifications/get_user_notification_choices/"


from .test_case_01 import TestCase01GetUserNotificationChoicesAPITestCase

__all__ = [
    "TestCase01GetUserNotificationChoicesAPITestCase"
]


