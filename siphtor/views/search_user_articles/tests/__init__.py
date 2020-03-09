# pylint: disable=wrong-import-position

APP_NAME = "phd3"
OPERATION_NAME = "search_user_articles"
REQUEST_METHOD = "post"
URL_SUFFIX = "users/search/follow/news/"

from .test_case_01 import TestCase01SearchUserArticlesAPITestCase

__all__ = [
    "TestCase01SearchUserArticlesAPITestCase"
]
