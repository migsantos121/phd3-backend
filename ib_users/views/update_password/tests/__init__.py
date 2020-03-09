# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "update_password"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/access_credentials/pwd/update/"


from .test_case_01 import TestCase01UpdatePasswordAPITestCase

__all__ = [
    "TestCase01UpdatePasswordAPITestCase"
]


