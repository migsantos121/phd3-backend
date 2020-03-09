# Endpoint Configuration

APP_NAME = "ib_comments"
OPERATION_NAME = "save_comment"
REQUEST_METHOD = "post"
URL_SUFFIX = "save_comment/"


from .test_case_01 import TestCase01SaveCommentAPITestCase

__all__ = [
    "TestCase01SaveCommentAPITestCase"
]


