from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase
from mock import mock

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

request_body = """
{
    "phone_number": "9160883373", 
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
        "securities": {"oauth": {"scopes": ["read"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password",
                                 "type": "oauth2"}},
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
        return ('a', 'b')

    @staticmethod
    def send_otp_sms(phone_number, country_code, otp_token):
        pass

    @staticmethod
    def send_otp_email(email, otp_token):
        pass

    @classmethod
    def validate_otp(cls, ib_user, otp_token, auth_type):
        pass


class TestCase01ResendOtpV2ForDataVerificationAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01ResendOtpV2ForDataVerificationAPITestCase, self).__init__(APP_NAME, OPERATION_NAME,
                                                                                  REQUEST_METHOD, URL_SUFFIX,
                                                                                  test_case,
                                                                                  *args, **kwargs)

    @mock.patch("ib_users.models.user_otp.UserOTP", UserOTP)
    def test_case(self):
        response = super(TestCase01ResendOtpV2ForDataVerificationAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)

    def setupUser(self, username, password):
        self.foo_user = self._create_user(username, password)

        self.foo_user.phone_number = "9160883374"
        self.foo_user.country_code = "91"
        self.foo_user.is_phone_verified = True
        self.foo_user.save()

        from ib_users.models import ChangeHistory

        from ib_users.constants.user_reg_type import UserRegistrationType
        ChangeHistory.objects.create(
            user_id=self.foo_user.id,
            old_val="91,9160883374",
            new_val="91,9160883373",
            is_verified=False,
            type=UserRegistrationType.PHONE_NUMBER.value
        )
