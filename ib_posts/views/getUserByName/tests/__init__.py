# Endpoint Configuration

APP_NAME = "ib_posts"
OPERATION_NAME = "getUserByName"
REQUEST_METHOD = "get"
URL_SUFFIX = "user/{username}/"


from .test_case_01 import TestCase01GetUserByNameAPITestCase

__all__ = [
    "TestCase01GetUserByNameAPITestCase"
]


