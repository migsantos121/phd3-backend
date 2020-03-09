from mock import mock

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "phone_number": "9160883374", 
    "auth_type": "phone_number", 
    "email": "", 
    "country_code": "91"
}
"""

response_body = """
{
    "success": true
}
"""

"""
Write your test case description here
"""

test_case = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}

class UserOTP():
    @classmethod
    def send_otp(cls, ib_user, auth_type):
        pass

    @classmethod
    def create_otp(cls, ib_user, auth_type):
        return ('a','b')

    @staticmethod
    def send_otp_sms(phone_number, country_code, otp_token):
        pass

    @staticmethod
    def send_otp_email(email, otp_token):
        pass

    @classmethod
    def validate_otp(cls, ib_user, otp_token, auth_type):
        pass

class TestCase01ResendOtpV2ForVerifiedAuthAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01ResendOtpV2ForVerifiedAuthAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    @mock.patch("ib_users.models.user_otp.UserOTP", UserOTP)
    def test_case(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.create(username="username", phone_number="9160883374", country_code="91", is_phone_verified=True)

        response = super(TestCase01ResendOtpV2ForVerifiedAuthAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


