# Endpoint Configuration

APP_NAME = "ib_social"
OPERATION_NAME = "get_inverse_relations"
REQUEST_METHOD = "post"
URL_SUFFIX = "member/get_inverse_relations/"


from .test_case_01 import TestCase01GetInverseRelationsAPITestCase

__all__ = [
    "TestCase01GetInverseRelationsAPITestCase"
]


