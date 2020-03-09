# Endpoint Configuration

APP_NAME = "ib_recommender"
OPERATION_NAME = "remove_user_category"
REQUEST_METHOD = "post"
URL_SUFFIX = "categories/{category_id}/"


from .test_case_01 import TestCase01RemoveUserCategoryAPITestCase

__all__ = [
    "TestCase01RemoveUserCategoryAPITestCase"
]


