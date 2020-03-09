# Endpoint Configuration

APP_NAME = "ib_notifications"
OPERATION_NAME = "get_user_notifications"
REQUEST_METHOD = "post"
URL_SUFFIX = "notifications/user_notifications/"


from .test_case_01 import TestCase01GetUserNotificationsAPITestCase

__all__ = [
    "TestCase01GetUserNotificationsAPITestCase"
]


