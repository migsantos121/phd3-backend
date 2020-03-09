# pylint: disable=wrong-import-position

APP_NAME = "phd3"
OPERATION_NAME = "get_article"
REQUEST_METHOD = "get"
URL_SUFFIX = "articles/{article_id}/"

from .test_case_01 import TestCase01GetArticleAPITestCase

__all__ = [
    "TestCase01GetArticleAPITestCase"
]
