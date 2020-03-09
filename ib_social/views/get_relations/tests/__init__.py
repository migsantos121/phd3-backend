# Endpoint Configuration

APP_NAME = "ib_social"
OPERATION_NAME = "get_relations"
REQUEST_METHOD = "post"
URL_SUFFIX = "member/get_relations/"


from .test_case_02 import TestCase02GetRelationsAPITestCase
from .test_case_01 import TestCase01GetRelationsAPITestCase

__all__ = [
    "TestCase02GetRelationsAPITestCase",
    "TestCase01GetRelationsAPITestCase"
]


