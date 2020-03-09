# pylint: disable=wrong-import-position

APP_NAME = "phd3"
OPERATION_NAME = "get_users_to_follow"
REQUEST_METHOD = "post"
URL_SUFFIX = "users/search/follow/"

from .test_case_01 import TestCase01GetUsersToFollowAPITestCase

__all__ = [
    "TestCase01GetUsersToFollowAPITestCase"
]
