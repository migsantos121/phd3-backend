# Endpoint Configuration

APP_NAME = "ib_notifications"
OPERATION_NAME = "deactivate_user_cm_tokens_api"
REQUEST_METHOD = "post"
URL_SUFFIX = "notifications/deactivate/"


from .test_case_01 import TestCase01DeactivateUserCmTokensApiAPITestCase

__all__ = [
    "TestCase01DeactivateUserCmTokensApiAPITestCase"
]


