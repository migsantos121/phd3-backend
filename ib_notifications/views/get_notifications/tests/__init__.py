# Endpoint Configuration

APP_NAME = "ib_notifications"
OPERATION_NAME = "get_notifications"
REQUEST_METHOD = "post"
URL_SUFFIX = "notifications/"


from .test_case_01 import TestCase01GetNotificationsAPITestCase

__all__ = [
    "TestCase01GetNotificationsAPITestCase"
]


