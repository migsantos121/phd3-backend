# Endpoint Configuration

APP_NAME = "ib_notifications"
OPERATION_NAME = "update_user_notification_choice"
REQUEST_METHOD = "post"
URL_SUFFIX = "notifications/update_user_notification_choice/"


from .test_case_01 import TestCase01UpdateUserNotificationChoiceAPITestCase

__all__ = [
    "TestCase01UpdateUserNotificationChoiceAPITestCase"
]


