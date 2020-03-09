# Endpoint Configuration

APP_NAME = "ib_articles"
OPERATION_NAME = "add_keywords"
REQUEST_METHOD = "post"
URL_SUFFIX = "keywords/add_keywords/"


from .test_case_01 import TestCase01AddKeywordsAPITestCase

__all__ = [
    "TestCase01AddKeywordsAPITestCase"
]


