# Endpoint Configuration

APP_NAME = "ib_posts"
OPERATION_NAME = "delete_post"
REQUEST_METHOD = "delete"
URL_SUFFIX = "posts/{post_id}/"


from .test_case_01 import TestCase01DeletePostAPITestCase

__all__ = [
    "TestCase01DeletePostAPITestCase"
]


