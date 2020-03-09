# Endpoint Configuration

APP_NAME = "ib_action"
OPERATION_NAME = "get_entities"
REQUEST_METHOD = "post"
URL_SUFFIX = "entities/"


from .test_case_01 import TestCase01GetEntitiesAPITestCase

__all__ = [
    "TestCase01GetEntitiesAPITestCase"
]


