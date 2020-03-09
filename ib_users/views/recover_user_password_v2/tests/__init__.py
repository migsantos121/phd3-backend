# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "recover_user_password_v2"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/recover_password/v2/"


from .test_case_02 import TestCase02RecoverUserPasswordV2APITestCase
from .test_case_01 import TestCase01RecoverUserPasswordV2APITestCase

__all__ = [
    "TestCase02RecoverUserPasswordV2APITestCase",
    "TestCase01RecoverUserPasswordV2APITestCase"
]


