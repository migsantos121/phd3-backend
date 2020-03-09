# Endpoint Configuration

APP_NAME = "ib_notifications"
OPERATION_NAME = "send_real_time_data_api"
REQUEST_METHOD = "post"
URL_SUFFIX = "send_real_time_data_api/v1/"


from .test_case_01 import TestCase01SendRealTimeDataApiAPITestCase

__all__ = [
    "TestCase01SendRealTimeDataApiAPITestCase"
]


