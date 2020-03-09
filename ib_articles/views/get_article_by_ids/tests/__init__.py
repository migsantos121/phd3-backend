# Endpoint Configuration

APP_NAME = "ib_articles"
OPERATION_NAME = "get_article_by_ids"
REQUEST_METHOD = "post"
URL_SUFFIX = "article/get_article_by_ids/"


from .test_case_01 import TestCase01GetArticleByIdsAPITestCase

__all__ = [
    "TestCase01GetArticleByIdsAPITestCase"
]


