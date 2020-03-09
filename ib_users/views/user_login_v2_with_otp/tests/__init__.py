# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "user_login_v2_with_otp"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/login/otp/v2/"


from .test_case_01 import TestCase01UserLoginV2WithOtpAPITestCase

__all__ = [
    "TestCase01UserLoginV2WithOtpAPITestCase"
]


