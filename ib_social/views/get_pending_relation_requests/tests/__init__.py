# Endpoint Configuration

APP_NAME = "ib_social"
OPERATION_NAME = "get_pending_relation_requests"
REQUEST_METHOD = "post"
URL_SUFFIX = "member/get_pending_relation_requests/"


from .test_case_01 import TestCase01GetPendingRelationRequestsAPITestCase

__all__ = [
    "TestCase01GetPendingRelationRequestsAPITestCase"
]


