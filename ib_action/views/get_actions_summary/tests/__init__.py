# Endpoint Configuration

APP_NAME = "ib_action"
OPERATION_NAME = "get_actions_summary"
REQUEST_METHOD = "post"
URL_SUFFIX = "summary/"


from .test_case_01 import TestCase01GetActionsSummaryAPITestCase

__all__ = [
    "TestCase01GetActionsSummaryAPITestCase"
]


