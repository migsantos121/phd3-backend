# Endpoint Configuration

APP_NAME = "ib_comments"
OPERATION_NAME = "report_comment"
REQUEST_METHOD = "post"
URL_SUFFIX = "report_comment/"


from .test_case_01 import TestCase01ReportCommentAPITestCase

__all__ = [
    "TestCase01ReportCommentAPITestCase"
]


