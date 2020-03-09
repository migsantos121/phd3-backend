# Endpoint Configuration

APP_NAME = "ib_posts"
OPERATION_NAME = "get_post"
REQUEST_METHOD = "get"
URL_SUFFIX = "posts/{post_id}/"


from .test_case_01 import TestCase01GetPostAPITestCase

__all__ = [
    "TestCase01GetPostAPITestCase"
]


