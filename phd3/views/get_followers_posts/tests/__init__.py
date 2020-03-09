# pylint: disable=wrong-import-position

APP_NAME = "phd3"
OPERATION_NAME = "get_followers_posts"
REQUEST_METHOD = "post"
URL_SUFFIX = "posts/followers/"

from .test_case_01 import TestCase01GetFollowersPostsAPITestCase

__all__ = [
    "TestCase01GetFollowersPostsAPITestCase"
]
