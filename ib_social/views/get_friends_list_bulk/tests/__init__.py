# Endpoint Configuration

APP_NAME = "ib_social"
OPERATION_NAME = "get_friends_list_bulk"
REQUEST_METHOD = "post"
URL_SUFFIX = "member/get_friends_list/bulk/"


from .test_case_01 import TestCase01GetFriendsListBulkAPITestCase

__all__ = [
    "TestCase01GetFriendsListBulkAPITestCase"
]


