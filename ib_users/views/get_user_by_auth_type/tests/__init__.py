# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "get_user_by_auth_type"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/get_user_by_auth_type/"


from .test_case_01 import TestCase01GetUserByAuthTypeAPITestCase

__all__ = [
    "TestCase01GetUserByAuthTypeAPITestCase"
]


