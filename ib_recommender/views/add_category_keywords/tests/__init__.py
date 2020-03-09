# Endpoint Configuration

APP_NAME = "ib_recommender"
OPERATION_NAME = "add_category_keywords"
REQUEST_METHOD = "post"
URL_SUFFIX = "categories/{category_id}/keywords/"


from .test_case_01 import TestCase01AddCategoryKeywordsAPITestCase

__all__ = [
    "TestCase01AddCategoryKeywordsAPITestCase"
]


