# Endpoint Configuration

APP_NAME = "ib_articles"
OPERATION_NAME = "update_article"
REQUEST_METHOD = "post"
URL_SUFFIX = "article/{article_id}/"


from .test_case_01 import TestCase01UpdateArticleAPITestCase

__all__ = [
    "TestCase01UpdateArticleAPITestCase"
]


