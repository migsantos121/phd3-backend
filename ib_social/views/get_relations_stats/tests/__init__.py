# Endpoint Configuration

APP_NAME = "ib_social"
OPERATION_NAME = "get_relations_stats"
REQUEST_METHOD = "post"
URL_SUFFIX = "relations/stats/"


from .test_case_01 import TestCase01GetRelationsStatsAPITestCase

__all__ = [
    "TestCase01GetRelationsStatsAPITestCase"
]


