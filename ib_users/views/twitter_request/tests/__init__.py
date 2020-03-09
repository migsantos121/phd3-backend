# pylint: disable=wrong-import-position

APP_NAME = "ib_users"
OPERATION_NAME = "twitter_request"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/twitter_request/"

from .test_case_01 import TestCase01TwitterRequestAPITestCase

__all__ = [
    "TestCase01TwitterRequestAPITestCase"
]
