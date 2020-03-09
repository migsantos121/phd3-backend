# Endpoint Configuration

APP_NAME = "ib_notifications"
OPERATION_NAME = "update_notification_status_as_read"
REQUEST_METHOD = "post"
URL_SUFFIX = "notifications/read/"


from .test_case_01 import TestCase01UpdateNotificationStatusAsReadAPITestCase

__all__ = [
    "TestCase01UpdateNotificationStatusAsReadAPITestCase"
]


