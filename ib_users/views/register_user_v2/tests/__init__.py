# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "register_user_v2"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/register/v2/"


from .test_case_02 import TestCase02RegisterUserV2APITestCase
from .test_case_03 import TestCase03RegisterUserV2APITestCase
from .test_case_01 import TestCase01RegisterUserV2APITestCase

__all__ = [
    "TestCase02RegisterUserV2APITestCase",
    "TestCase03RegisterUserV2APITestCase",
    "TestCase01RegisterUserV2APITestCase"
]


