# Endpoint Configuration

APP_NAME = "ib_recommender"
OPERATION_NAME = "get_user_categories"
REQUEST_METHOD = "get"
URL_SUFFIX = "categories/"


from .test_case_01 import TestCase01GetUserCategoriesAPITestCase

__all__ = [
    "TestCase01GetUserCategoriesAPITestCase"
]


