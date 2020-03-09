# Endpoint Configuration

APP_NAME = "ib_social"
OPERATION_NAME = "delink_user_social_account"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/delink_social_account/"


from .test_case_01 import TestCase01DelinkUserSocialAccountAPITestCase

__all__ = [
    "TestCase01DelinkUserSocialAccountAPITestCase"
]


