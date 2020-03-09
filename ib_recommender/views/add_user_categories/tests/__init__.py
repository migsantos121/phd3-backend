# Endpoint Configuration

APP_NAME = "ib_recommender"
OPERATION_NAME = "add_user_categories"
REQUEST_METHOD = "post"
URL_SUFFIX = "categories/"


from .test_case_01 import TestCase01AddUserCategoriesAPITestCase

__all__ = [
    "TestCase01AddUserCategoriesAPITestCase"
]


