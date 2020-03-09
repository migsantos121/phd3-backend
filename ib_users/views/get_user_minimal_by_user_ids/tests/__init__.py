# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "get_user_minimal_by_user_ids"
REQUEST_METHOD = "post"
URL_SUFFIX = "users/minimal_details/"


from .test_case_01 import TestCase01GetUserMinimalByUserIdsAPITestCase

__all__ = [
    "TestCase01GetUserMinimalByUserIdsAPITestCase"
]


