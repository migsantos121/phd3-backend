# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "login_user_v2"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/login/v2/"


from .test_case_02 import TestCase02LoginUserV2APITestCase
from .test_case_03 import TestCase03LoginUserV2APITestCase
from .test_case_01 import TestCase01LoginUserV2APITestCase

__all__ = [
    "TestCase02LoginUserV2APITestCase",
    "TestCase03LoginUserV2APITestCase",
    "TestCase01LoginUserV2APITestCase"
]


