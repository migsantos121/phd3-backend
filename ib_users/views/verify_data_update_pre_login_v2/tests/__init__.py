# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "verify_data_update_pre_login_v2"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/verify_data_update_pre_login/v2/"


from .test_case_02 import TestCase02VerifyDataUpdatePreLoginV2APITestCase
from .test_case_01 import TestCase01VerifyDataUpdatePreLoginV2APITestCase

__all__ = [
    "TestCase02VerifyDataUpdatePreLoginV2APITestCase",
    "TestCase01VerifyDataUpdatePreLoginV2APITestCase"
]


