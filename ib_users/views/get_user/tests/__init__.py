# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "get_user"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/"


from .test_case_01 import TestCase01GetUserAPITestCase

__all__ = [
    "TestCase01GetUserAPITestCase"
]


