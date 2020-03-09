# Endpoint Configuration

APP_NAME = "ib_articles"
OPERATION_NAME = "add_article"
REQUEST_METHOD = "post"
URL_SUFFIX = "article/add_article/"


from .test_case_01 import TestCase01AddArticleAPITestCase

__all__ = [
    "TestCase01AddArticleAPITestCase"
]


