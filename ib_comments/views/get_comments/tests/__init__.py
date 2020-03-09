# Endpoint Configuration

APP_NAME = "ib_comments"
OPERATION_NAME = "get_comments"
REQUEST_METHOD = "post"
URL_SUFFIX = "get_comments/"


from .test_case_01 import TestCase01GetCommentsAPITestCase

__all__ = [
    "TestCase01GetCommentsAPITestCase"
]


