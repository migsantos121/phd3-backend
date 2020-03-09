# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "set_password"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/access_credentials/set_password/"


from .test_case_01 import TestCase01SetPasswordAPITestCase

__all__ = [
    "TestCase01SetPasswordAPITestCase"
]


