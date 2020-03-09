# Endpoint Configuration

APP_NAME = "ib_recommender"
OPERATION_NAME = "get_user_category"
REQUEST_METHOD = "get"
URL_SUFFIX = "categories/{category_id}/"


from .test_case_01 import TestCase01GetUserCategoryAPITestCase

__all__ = [
    "TestCase01GetUserCategoryAPITestCase"
]


