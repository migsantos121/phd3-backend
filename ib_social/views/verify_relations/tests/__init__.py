# Endpoint Configuration

APP_NAME = "ib_social"
OPERATION_NAME = "verify_relations"
REQUEST_METHOD = "post"
URL_SUFFIX = "member/verify_relations/"


from .test_case_01 import TestCase01VerifyRelationsAPITestCase

__all__ = [
    "TestCase01VerifyRelationsAPITestCase"
]


