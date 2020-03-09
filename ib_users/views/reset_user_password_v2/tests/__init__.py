# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "reset_user_password_v2"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/reset_password/v2/"


from .test_case_02 import TestCase02ResetUserPasswordV2APITestCase
from .test_case_01 import TestCase01ResetUserPasswordV2APITestCase

__all__ = [
    "TestCase02ResetUserPasswordV2APITestCase",
    "TestCase01ResetUserPasswordV2APITestCase"
]


