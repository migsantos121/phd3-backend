# Endpoint Configuration

APP_NAME = "ib_action"
OPERATION_NAME = "user_action_counts"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/actions/counts/"


from .test_case_01 import TestCase01UserActionCountsAPITestCase

__all__ = [
    "TestCase01UserActionCountsAPITestCase"
]


