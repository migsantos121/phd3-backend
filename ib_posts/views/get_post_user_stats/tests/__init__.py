# Endpoint Configuration

APP_NAME = "ib_posts"
OPERATION_NAME = "get_post_user_stats"
REQUEST_METHOD = "get"
URL_SUFFIX = "user/posts/stats/"


from .test_case_01 import TestCase01GetPostUserStatsAPITestCase

__all__ = [
    "TestCase01GetPostUserStatsAPITestCase"
]


