# Endpoint Configuration

APP_NAME = "ib_comments"
OPERATION_NAME = "delete_comment"
REQUEST_METHOD = "post"
URL_SUFFIX = "delete_comment/"


from .test_case_01 import TestCase01DeleteCommentAPITestCase

__all__ = [
    "TestCase01DeleteCommentAPITestCase"
]


