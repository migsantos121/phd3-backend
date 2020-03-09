# Endpoint Configuration

APP_NAME = "ib_articles"
OPERATION_NAME = "get_keywords"
REQUEST_METHOD = "post"
URL_SUFFIX = "keywords/"


from .test_case_01 import TestCase01GetKeywordsAPITestCase

__all__ = [
    "TestCase01GetKeywordsAPITestCase"
]


