# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "link_user_social_account"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/link_social_account/"


from .test_case_01 import TestCase01LinkUserSocialAccountAPITestCase

__all__ = [
    "TestCase01LinkUserSocialAccountAPITestCase"
]


