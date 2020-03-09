# Endpoint Configuration

APP_NAME = "ib_notifications"
OPERATION_NAME = "add_user_token"
REQUEST_METHOD = "post"
URL_SUFFIX = "notifications/add_user_token/"


from .test_case_01 import TestCase01AddUserTokenAPITestCase

__all__ = [
    "TestCase01AddUserTokenAPITestCase"
]


