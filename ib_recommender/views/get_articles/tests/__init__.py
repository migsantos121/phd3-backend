# Endpoint Configuration

APP_NAME = "ib_recommender"
OPERATION_NAME = "get_articles"
REQUEST_METHOD = "post"
URL_SUFFIX = "articles/"


from .test_case_01 import TestCase01GetArticlesAPITestCase

__all__ = [
    "TestCase01GetArticlesAPITestCase"
]


