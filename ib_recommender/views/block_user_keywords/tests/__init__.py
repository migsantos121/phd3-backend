# Endpoint Configuration

APP_NAME = "ib_recommender"
OPERATION_NAME = "block_user_keywords"
REQUEST_METHOD = "post"
URL_SUFFIX = "keywords/block/"


from .test_case_01 import TestCase01BlockUserKeywordsAPITestCase

__all__ = [
    "TestCase01BlockUserKeywordsAPITestCase"
]


