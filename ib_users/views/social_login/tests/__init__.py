# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "social_login"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/social_login/"


from .test_case_02 import TestCase02SocialLoginAPITestCase
from .test_case_03 import TestCase03SocialLoginAPITestCase
from .test_case_01 import TestCase01SocialLoginAPITestCase

__all__ = [
    "TestCase02SocialLoginAPITestCase",
    "TestCase03SocialLoginAPITestCase",
    "TestCase01SocialLoginAPITestCase"
]


