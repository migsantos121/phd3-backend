# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "user_logout"
REQUEST_METHOD = "get"
URL_SUFFIX = "user/user_logout/"


from .test_case_01 import TestCase01UserLogoutAPITestCase

__all__ = [
    "TestCase01UserLogoutAPITestCase"
]


