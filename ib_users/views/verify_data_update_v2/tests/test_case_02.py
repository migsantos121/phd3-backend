import time

from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from ib_users.models.ib_user import IBUser
from ib_users.models.user_otp import UserOTP
from ib_users.utilities.crypto import hash_otp
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

request_body = """
{
  "auth_type": "email",
  "email": "user@email.com",
  "country_code": "+91",
  "phone_number": "8437479642",
  "verify_token": "123456"
}
"""

response_body = """
{"success": true}
"""

test_case = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["write"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password",
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
    def send_otp(cls, ib_user, auth_type, phone_number=None, country_code=None,
                 email=None):
        pass

    @classmethod
    def create_otp(cls, ib_user, auth_type):
        return ('a', 'b',)

    @staticmethod
    def send_otp_sms(phone_number, country_code, otp_token):
        pass

    @staticmethod
    def send_otp_email(email, otp_token):
        pass

    @classmethod
    def validate_otp(cls, ib_user, otp_token, auth_type):
        return True


from mock import mock


class TestCase02VerifyDataUpdateV2APITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase02VerifyDataUpdateV2APITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD,
                                                                      URL_SUFFIX, test_case,
                                                                      *args, **kwargs)

    @mock.patch('ib_users.models.user_otp.UserOTP', UserOTP)
    def test_case(self):
        user = IBUser.objects.create(phone_number='1234567890',
                                     username='new_user',
                                     country_code='+91',
                                     email='user@email.com',
                                     password='password123',
                                     dob='2012-02-02 12:21',
                                     is_email_verified=True)

        user_otp = UserOTP(ib_user=user,
                           otp_token=hash_otp('123456'),
                           auth_type='email',
                           expiry_time=int(time.time()),
                           is_active=True)
        user_otp.reset_expiry_time()

        response = super(TestCase02VerifyDataUpdateV2APITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)

    def setupUser(self, username, password):
        super(TestCase02VerifyDataUpdateV2APITestCase, self).setupUser(username, password)

        self.foo_user.first_name = "user"
        self.foo_user.id = 1

    def setupOAuth(self, scopes):
        super(TestCase02VerifyDataUpdateV2APITestCase, self).setupOAuth(scopes)
