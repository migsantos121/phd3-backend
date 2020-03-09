# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "resend_otp_v2_for_data_verification"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/auth/update/otp/resend/v2/"


from .test_case_01 import TestCase01ResendOtpV2ForDataVerificationAPITestCase

__all__ = [
    "TestCase01ResendOtpV2ForDataVerificationAPITestCase"
]


