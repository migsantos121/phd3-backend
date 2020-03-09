# Endpoint Configuration

APP_NAME = "ib_articles"
OPERATION_NAME = "delete_article"
REQUEST_METHOD = "delete"
URL_SUFFIX = "article/{article_id}/"


from .test_case_01 import TestCase01DeleteArticleAPITestCase

__all__ = [
    "TestCase01DeleteArticleAPITestCase"
]


