# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "get_user_supported_languages_api"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/get_supported_languages/"


from .test_case_01 import TestCase01GetUserSupportedLanguagesApiAPITestCase

__all__ = [
    "TestCase01GetUserSupportedLanguagesApiAPITestCase"
]


