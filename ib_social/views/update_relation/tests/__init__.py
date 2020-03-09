# Endpoint Configuration

APP_NAME = "ib_social"
OPERATION_NAME = "update_relation"
REQUEST_METHOD = "post"
URL_SUFFIX = "member/update_relation/"


from .test_case_04 import TestCase04UpdateRelationAPITestCase
from .test_case_02 import TestCase02UpdateRelationAPITestCase
from .test_case_03 import TestCase03UpdateRelationAPITestCase
from .test_case_01 import TestCase01UpdateRelationAPITestCase

__all__ = [
    "TestCase04UpdateRelationAPITestCase",
    "TestCase02UpdateRelationAPITestCase",
    "TestCase03UpdateRelationAPITestCase",
    "TestCase01UpdateRelationAPITestCase"
]


