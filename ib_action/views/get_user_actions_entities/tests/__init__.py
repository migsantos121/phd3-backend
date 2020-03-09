# Endpoint Configuration

APP_NAME = "ib_action"
OPERATION_NAME = "get_user_actions_entities"
REQUEST_METHOD = "post"
URL_SUFFIX = "users/actions/entities/v2/"


from .test_case_01 import TestCase01GetUserActionsEntitiesAPITestCase

__all__ = [
    "TestCase01GetUserActionsEntitiesAPITestCase"
]


