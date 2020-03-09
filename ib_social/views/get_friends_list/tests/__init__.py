# Endpoint Configuration

APP_NAME = "ib_social"
OPERATION_NAME = "get_friends_list"
REQUEST_METHOD = "post"
URL_SUFFIX = "member/get_friends_list/"


from .test_case_01 import TestCase01GetFriendsListAPITestCase

__all__ = [
    "TestCase01GetFriendsListAPITestCase"
]


