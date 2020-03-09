# Endpoint Configuration

APP_NAME = "ib_action"
OPERATION_NAME = "add_action"
REQUEST_METHOD = "post"
URL_SUFFIX = "action/"


from .test_case_04 import TestCase04AddActionAPITestCase
from .test_case_05 import TestCase05AddActionAPITestCase
from .test_case_02 import TestCase02AddActionAPITestCase
from .test_case_03 import TestCase03AddActionAPITestCase
from .test_case_01 import TestCase01AddActionAPITestCase

__all__ = [
    "TestCase04AddActionAPITestCase",
    "TestCase05AddActionAPITestCase",
    "TestCase02AddActionAPITestCase",
    "TestCase03AddActionAPITestCase",
    "TestCase01AddActionAPITestCase"
]


