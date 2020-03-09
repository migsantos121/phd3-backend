# Endpoint Configuration

APP_NAME = "ib_posts"
OPERATION_NAME = "get_posts_by_user_id"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/posts/"


from .test_case_01 import TestCase01GetPostsByUserIdAPITestCase

__all__ = [
    "TestCase01GetPostsByUserIdAPITestCase"
]


