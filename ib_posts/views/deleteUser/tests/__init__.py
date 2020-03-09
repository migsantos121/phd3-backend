# Endpoint Configuration

APP_NAME = "ib_posts"
OPERATION_NAME = "deleteUser"
REQUEST_METHOD = "delete"
URL_SUFFIX = "user/{username}/"


from .test_case_01 import TestCase01DeleteUserAPITestCase

__all__ = [
    "TestCase01DeleteUserAPITestCase"
]


