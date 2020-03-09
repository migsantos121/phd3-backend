# Endpoint Configuration

APP_NAME = "ib_posts"
OPERATION_NAME = "get_posts"
REQUEST_METHOD = "post"
URL_SUFFIX = "posts/"


from .test_case_01 import TestCase01GetPostsAPITestCase

__all__ = [
    "TestCase01GetPostsAPITestCase"
]


