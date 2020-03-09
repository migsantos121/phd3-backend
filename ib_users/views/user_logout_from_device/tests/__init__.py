# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "user_logout_from_device"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/user_logout/"


from .test_case_01 import TestCase01UserLogoutFromDeviceAPITestCase

__all__ = [
    "TestCase01UserLogoutFromDeviceAPITestCase"
]


