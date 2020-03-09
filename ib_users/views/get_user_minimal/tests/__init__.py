# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "get_user_minimal"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/minimal_details/"


from .test_case_01 import TestCase01GetUserMinimalAPITestCase

__all__ = [
    "TestCase01GetUserMinimalAPITestCase"
]


