# Endpoint Configuration

APP_NAME = "ib_action"
OPERATION_NAME = "get_saved_items"
REQUEST_METHOD = "post"
URL_SUFFIX = "users/actions/get_saved_items/"


from .test_case_01 import TestCase01GetSavedItemsAPITestCase

__all__ = [
    "TestCase01GetSavedItemsAPITestCase"
]


