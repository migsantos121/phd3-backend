# Endpoint Configuration

APP_NAME = "ib_articles"
OPERATION_NAME = "add_news_source"
REQUEST_METHOD = "post"
URL_SUFFIX = "news_sources/"


from .test_case_01 import TestCase01AddNewsSourceAPITestCase

__all__ = [
    "TestCase01AddNewsSourceAPITestCase"
]


