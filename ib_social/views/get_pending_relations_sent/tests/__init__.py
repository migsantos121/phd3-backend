# Endpoint Configuration

APP_NAME = "ib_social"
OPERATION_NAME = "get_pending_relations_sent"
REQUEST_METHOD = "post"
URL_SUFFIX = "member/get_pending_relations_sent/"


from .test_case_01 import TestCase01GetPendingRelationsSentAPITestCase

__all__ = [
    "TestCase01GetPendingRelationsSentAPITestCase"
]


