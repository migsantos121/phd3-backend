# Endpoint Configuration

APP_NAME = "ib_social"
OPERATION_NAME = "friends_with_relation"
REQUEST_METHOD = "post"
URL_SUFFIX = "friends_with_relation/"


from .test_case_01 import TestCase01FriendsWithRelationAPITestCase

__all__ = [
    "TestCase01FriendsWithRelationAPITestCase"
]


