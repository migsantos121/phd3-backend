# Endpoint Configuration

APP_NAME = "ib_posts"
OPERATION_NAME = "update_post"
REQUEST_METHOD = "post"
URL_SUFFIX = "posts/{post_id}/"


from .test_case_01 import TestCase01UpdatePostAPITestCase

__all__ = [
    "TestCase01UpdatePostAPITestCase"
]


