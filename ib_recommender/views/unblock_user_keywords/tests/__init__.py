# Endpoint Configuration

APP_NAME = "ib_recommender"
OPERATION_NAME = "unblock_user_keywords"
REQUEST_METHOD = "post"
URL_SUFFIX = "keywords/unblock/"


from .test_case_01 import TestCase01UnblockUserKeywordsAPITestCase

__all__ = [
    "TestCase01UnblockUserKeywordsAPITestCase"
]


