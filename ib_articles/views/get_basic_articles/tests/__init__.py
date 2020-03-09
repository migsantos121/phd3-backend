# Endpoint Configuration

APP_NAME = "ib_articles"
OPERATION_NAME = "get_basic_articles"
REQUEST_METHOD = "post"
URL_SUFFIX = "article/basic/"


from .test_case_01 import TestCase01GetBasicArticlesAPITestCase

__all__ = [
    "TestCase01GetBasicArticlesAPITestCase"
]


