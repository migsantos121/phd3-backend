# Endpoint Configuration

APP_NAME = "ib_posts"
OPERATION_NAME = "updateUser"
REQUEST_METHOD = "put"
URL_SUFFIX = "user/{username}/"


from .test_case_01 import TestCase01UpdateUserAPITestCase

__all__ = [
    "TestCase01UpdateUserAPITestCase"
]


