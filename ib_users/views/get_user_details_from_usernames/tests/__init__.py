# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "get_user_details_from_usernames"
REQUEST_METHOD = "post"
URL_SUFFIX = "users/usernames/"


from .test_case_01 import TestCase01GetUserDetailsFromUsernamesAPITestCase

__all__ = [
    "TestCase01GetUserDetailsFromUsernamesAPITestCase"
]


