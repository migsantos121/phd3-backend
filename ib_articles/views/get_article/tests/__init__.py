# pylint: disable=wrong-import-position

APP_NAME = "ib_articles"
OPERATION_NAME = "get_articles"
REQUEST_METHOD = "post"
URL_SUFFIX = "article/articles/"

from .test_case_01 import TestCase01GetArticlesAPITestCase

__all__ = [
    "TestCase01GetArticlesAPITestCase"
]
