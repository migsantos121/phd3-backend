# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "get_user_language_preference"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/language/"


from .test_case_01 import TestCase01GetUserLanguagePreferenceAPITestCase

__all__ = [
    "TestCase01GetUserLanguagePreferenceAPITestCase"
]


