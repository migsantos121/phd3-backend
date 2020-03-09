# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "get_users"
REQUEST_METHOD = "post"
URL_SUFFIX = "users/"


from .test_case_01 import TestCase01GetUsersAPITestCase

__all__ = [
    "TestCase01GetUsersAPITestCase"
]


