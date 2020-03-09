# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "activate_or_deactivate_account"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/activate_or_deactivate_account/"


from .test_case_01 import TestCase01ActivateOrDeactivateAccountAPITestCase

__all__ = [
    "TestCase01ActivateOrDeactivateAccountAPITestCase"
]


