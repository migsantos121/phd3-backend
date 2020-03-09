# Endpoint Configuration

APP_NAME = "ib_notifications"
OPERATION_NAME = "get_groups"
REQUEST_METHOD = "post"
URL_SUFFIX = "notifications/groups/"


from .test_case_01 import TestCase01GetGroupsAPITestCase

__all__ = [
    "TestCase01GetGroupsAPITestCase"
]


