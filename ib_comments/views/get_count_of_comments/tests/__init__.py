# Endpoint Configuration

APP_NAME = "ib_comments"
OPERATION_NAME = "get_count_of_comments"
REQUEST_METHOD = "post"
URL_SUFFIX = "get_count_of_comments/"


from .test_case_01 import TestCase01GetCountOfCommentsAPITestCase

__all__ = [
    "TestCase01GetCountOfCommentsAPITestCase"
]


