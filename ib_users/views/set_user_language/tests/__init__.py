# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "set_user_language"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/set_language/"


from .test_case_01 import TestCase01SetUserLanguageAPITestCase

__all__ = [
    "TestCase01SetUserLanguageAPITestCase"
]


