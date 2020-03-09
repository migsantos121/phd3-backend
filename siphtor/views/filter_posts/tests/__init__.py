# pylint: disable=wrong-import-position

APP_NAME = "phd3"
OPERATION_NAME = "filter_posts"
REQUEST_METHOD = "post"
URL_SUFFIX = "posts/filter/"

from .test_case_01 import TestCase01FilterPostsAPITestCase

__all__ = [
    "TestCase01FilterPostsAPITestCase"
]
