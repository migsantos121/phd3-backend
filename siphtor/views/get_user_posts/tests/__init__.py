# Endpoint Configuration

APP_NAME = "phd3"
OPERATION_NAME = "get_user_posts"
REQUEST_METHOD = "post"
URL_SUFFIX = "posts/"


from .test_case_01 import TestCase01GetUserPostsAPITestCase

__all__ = [
    "TestCase01GetUserPostsAPITestCase"
]


