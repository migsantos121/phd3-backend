# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "update_user_details"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/update/"


from .test_case_01 import TestCase01UpdateUserDetailsAPITestCase

__all__ = [
    "TestCase01UpdateUserDetailsAPITestCase"
]


