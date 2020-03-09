# Endpoint Configuration

APP_NAME = "phd3"
OPERATION_NAME = "filter_articles"
REQUEST_METHOD = "post"
URL_SUFFIX = "articles/filter/"


from .test_case_01 import TestCase01FilterArticlesAPITestCase

__all__ = [
    "TestCase01FilterArticlesAPITestCase"
]


