# Endpoint Configuration

APP_NAME = "ib_action"
OPERATION_NAME = "get_user_action_entities"
REQUEST_METHOD = "post"
URL_SUFFIX = "users/actions/entities/"


from .test_case_01 import TestCase01GetUserActionEntitiesAPITestCase

__all__ = [
    "TestCase01GetUserActionEntitiesAPITestCase"
]


