# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "check_username_availability"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/availability/username/"


from .test_case_01 import TestCase01CheckUsernameAvailabilityAPITestCase

__all__ = [
    "TestCase01CheckUsernameAvailabilityAPITestCase"
]


