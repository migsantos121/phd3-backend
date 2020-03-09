# Endpoint Configuration

APP_NAME = "ib_social"
OPERATION_NAME = "update_relation_status"
REQUEST_METHOD = "post"
URL_SUFFIX = "member/update_relation_status/"


from .test_case_01 import TestCase01UpdateRelationStatusAPITestCase

__all__ = [
    "TestCase01UpdateRelationStatusAPITestCase"
]


