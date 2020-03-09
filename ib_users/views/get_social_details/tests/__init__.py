# Endpoint Configuration

APP_NAME = "ib_users"
OPERATION_NAME = "get_social_details"
REQUEST_METHOD = "post"
URL_SUFFIX = "user/get_social_details/"


from .test_case_01 import TestCase01GetSocialDetailsAPITestCase

__all__ = [
    "TestCase01GetSocialDetailsAPITestCase"
]


