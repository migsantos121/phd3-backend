# Endpoint Configuration

APP_NAME = "phd3"
OPERATION_NAME = "get_user_articles"
REQUEST_METHOD = "post"
URL_SUFFIX = "articles/"


from .test_case_01 import TestCase01GetUserArticlesAPITestCase

__all__ = [
    "TestCase01GetUserArticlesAPITestCase"
]


