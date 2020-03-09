# Endpoint Configuration

APP_NAME = "ib_recommender"
OPERATION_NAME = "get_user_keywords"
REQUEST_METHOD = "post"
URL_SUFFIX = "keywords/"


from .test_case_01 import TestCase01GetUserKeywordsAPITestCase

__all__ = [
    "TestCase01GetUserKeywordsAPITestCase"
]


