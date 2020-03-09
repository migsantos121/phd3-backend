# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "verify_data_update_v2"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/verify_data_update/v2/"


from .test_case_02 import TestCase02VerifyDataUpdateV2APITestCase
from .test_case_01 import TestCase01VerifyDataUpdateV2APITestCase

__all__ = [
    "TestCase02VerifyDataUpdateV2APITestCase",
    "TestCase01VerifyDataUpdateV2APITestCase"
]


