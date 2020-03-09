# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "update_user_details_with_verification"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/update_data/v2/"


from .test_case_01 import TestCase01UpdateUserDetailsWithVerificationAPITestCase

__all__ = [
    "TestCase01UpdateUserDetailsWithVerificationAPITestCase"
]


