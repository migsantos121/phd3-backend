# Endpoint Configuration

APP_NAME = "ib_posts"
OPERATION_NAME = "add_post"
REQUEST_METHOD = "post"
URL_SUFFIX = "posts/add_post/"


from .test_case_01 import TestCase01AddPostAPITestCase

__all__ = [
    "TestCase01AddPostAPITestCase"
]


