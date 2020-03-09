# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "search_user_by_auth_type"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/search_by_auth_type/"


from .test_case_01 import TestCase01SearchUserByAuthTypeAPITestCase

__all__ = [
    "TestCase01SearchUserByAuthTypeAPITestCase"
]


