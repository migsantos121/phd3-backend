# Endpoint Configuration

APP_NAME = "ib_notifications"
OPERATION_NAME = "add_member_to_group"
REQUEST_METHOD = "post"
URL_SUFFIX = "notifications/add_member_to_group/"


from .test_case_01 import TestCase01AddMemberToGroupAPITestCase

__all__ = [
    "TestCase01AddMemberToGroupAPITestCase"
]


