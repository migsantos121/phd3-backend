# Endpoint Configuration

APP_NAME = "phd3"
OPERATION_NAME = "get_people"
REQUEST_METHOD = "post"
URL_SUFFIX = "people/"


from .test_case_01 import TestCase01GetPeopleAPITestCase

__all__ = [
    "TestCase01GetPeopleAPITestCase"
]


