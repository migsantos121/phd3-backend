# Endpoint Configuration

APP_NAME = "ib_action"
OPERATION_NAME = "get_users_actions_summary"
REQUEST_METHOD = "post"
URL_SUFFIX = "summary/users/"


from .test_case_02 import TestCase02GetUsersActionsSummaryAPITestCase
from .test_case_03 import TestCase03GetUsersActionsSummaryAPITestCase
from .test_case_01 import TestCase01GetUsersActionsSummaryAPITestCase

__all__ = [
    "TestCase02GetUsersActionsSummaryAPITestCase",
    "TestCase03GetUsersActionsSummaryAPITestCase",
    "TestCase01GetUsersActionsSummaryAPITestCase"
]


