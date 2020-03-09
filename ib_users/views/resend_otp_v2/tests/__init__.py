# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "resend_otp_v2"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/access_credentials/otp/resend/v2/"


from .test_case_01 import TestCase01ResendOtpV2APITestCase

__all__ = [
    "TestCase01ResendOtpV2APITestCase"
]


