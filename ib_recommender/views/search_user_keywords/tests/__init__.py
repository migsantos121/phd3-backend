# Endpoint Configuration

APP_NAME = "ib_recommender"
OPERATION_NAME = "search_user_keywords"
REQUEST_METHOD = "post"
URL_SUFFIX = "keywords/search/"


from .test_case_01 import TestCase01SearchUserKeywordsAPITestCase

__all__ = [
    "TestCase01SearchUserKeywordsAPITestCase"
]


