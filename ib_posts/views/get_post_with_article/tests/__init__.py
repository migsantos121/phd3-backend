# Endpoint Configuration

APP_NAME = "ib_posts"
OPERATION_NAME = "get_post_with_article"
REQUEST_METHOD = "get"
URL_SUFFIX = "posts/{post_id}/article/"


from .test_case_01 import TestCase01GetPostWithArticleAPITestCase

__all__ = [
    "TestCase01GetPostWithArticleAPITestCase"
]


