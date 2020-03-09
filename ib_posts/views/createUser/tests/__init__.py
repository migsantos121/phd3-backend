# Endpoint Configuration

APP_NAME = "ib_posts"
OPERATION_NAME = "createUser"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/"


from .test_case_01 import TestCase01CreateUserAPITestCase

__all__ = [
    "TestCase01CreateUserAPITestCase"
]


