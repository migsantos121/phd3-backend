# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "resend_otp_v2_for_verified_auth"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/login/otp/resend/v2/"


from .test_case_01 import TestCase01ResendOtpV2ForVerifiedAuthAPITestCase

__all__ = [
    "TestCase01ResendOtpV2ForVerifiedAuthAPITestCase"
]


