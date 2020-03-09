# Endpoint Configuration

APP_NAME = "ib_notifications"
OPERATION_NAME = "send_notification"
REQUEST_METHOD = "post"
URL_SUFFIX = "notifications/send_notification/"


from .test_case_01 import TestCase01SendNotificationAPITestCase

__all__ = [
    "TestCase01SendNotificationAPITestCase"
]


