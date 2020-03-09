# Endpoint Configuration

APP_NAME = "ib_recommender"
OPERATION_NAME = "remove_category_keywords"
REQUEST_METHOD = "post"
URL_SUFFIX = "categories/{category_id}/keywords/remove/"


from .test_case_01 import TestCase01RemoveCategoryKeywordsAPITestCase

__all__ = [
    "TestCase01RemoveCategoryKeywordsAPITestCase"
]


