# Endpoint Configuration

APP_NAME = "phd3"
OPERATION_NAME = "get_user_stats"
REQUEST_METHOD = "get"
URL_SUFFIX = "user/stats/"


from .test_case_01 import TestCase01GetUserStatsAPITestCase

__all__ = [
    "TestCase01GetUserStatsAPITestCase"
]


