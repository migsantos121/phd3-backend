# pylint: disable=wrong-import-position

APP_NAME = "ib_users"
OPERATION_NAME = "twitter_response"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/twitter_response/"

from .test_case_01 import TestCase01TwitterResponseAPITestCase

__all__ = [
    "TestCase01TwitterResponseAPITestCase"
]
