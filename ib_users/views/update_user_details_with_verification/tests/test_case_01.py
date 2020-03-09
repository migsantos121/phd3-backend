from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import \
    CustomAPITestCase
from mock import mock

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

request_body = """
[
    {
        "phone_number": "9160883374", 
        "country_code": "91", 
        "update_type": "phone_number"
    }
]
"""

response_body = """
{"success": true}
"""

"""
if two users tried to change to same mobile no
"""

test_case = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["write"],
                                 "tokenUrl": "http://auth.ibtspl.com/oauth2/",
                                 "flow": "password", "type": "oauth2"}},
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
    def send_otp(cls, ib_user, auth_type, phone_number, country_code):
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


class TestCase01UpdateUserDetailsWithVerificationAPITestCase(
    CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01UpdateUserDetailsWithVerificationAPITestCase,
              self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD,
                             URL_SUFFIX, test_case,
                             *args, **kwargs)

    @mock.patch("ib_users.models.user_otp.UserOTP", UserOTP)
    def test_case(self):
        from ib_users.models import ChangeHistory
        from ib_users.constants.user_reg_type import UserRegistrationType
        ChangeHistory.objects.create(
            user_id=2,
            old_val='',
            new_val="91,9160883374",
            is_verified=False,
            type=UserRegistrationType.PHONE_NUMBER.value

        )

        response = super(
            TestCase01UpdateUserDetailsWithVerificationAPITestCase,
            self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)
        ChangeHistory.objects.get(
            new_val="91,9160883374",
            is_verified=False,
            type=UserRegistrationType.PHONE_NUMBER.value
        )
