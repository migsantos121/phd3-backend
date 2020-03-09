# Endpoint Configuration

APP_NAME = "ib_action"
OPERATION_NAME = "get_friends_actions"
REQUEST_METHOD = "post"
URL_SUFFIX = "get_friends_actions/"


from .test_case_01 import TestCase01GetFriendsActionsAPITestCase

__all__ = [
    "TestCase01GetFriendsActionsAPITestCase"
]


