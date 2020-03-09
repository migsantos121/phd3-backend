# Endpoint Configuration

APP_NAME = "ib_articles"
OPERATION_NAME = "get_article_by_url"
REQUEST_METHOD = "post"
URL_SUFFIX = "articles/url/"


from .test_case_01 import TestCase01GetArticleByUrlAPITestCase

__all__ = [
    "TestCase01GetArticleByUrlAPITestCase"
]


