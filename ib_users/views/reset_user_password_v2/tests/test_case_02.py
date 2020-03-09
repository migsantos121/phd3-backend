import time

from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from ib_users.models.ib_user import IBUser
from ib_users.models.user_otp import UserOTP
from ib_users.utilities.crypto import hash_otp
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

request_body = """
{
    "auth_type": "email", 
    "username": "", 
    "country_code": "+91", 
    "token": "123456", 
    "client_id": "app_id", 
    "client_secret": "app_secret", 
    "password": "password123", 
    "phone_number": "1234567890", 
    "email": "user@email.com"
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


class TestCase02ResetUserPasswordV2APITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase02ResetUserPasswordV2APITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    @mock.patch('ib_users.models.user_otp.UserOTP', UserOTP)
    def test_case(self):
        from oauth2_provider.models import Application
        Application.objects.create(client_id='app_id', client_secret='app_secret', user_id=1)

        user = IBUser.objects.create(phone_number='1234567890',
                                     username='new_user',
                                     country_code='+91',
                                     password='password123',
                                     dob='2012-02-02 12:21',
                                     email='user@email.com',
                                     is_email_verified=True)

        user_otp = UserOTP(ib_user=user,
                           otp_token=hash_otp('123456'),
                           auth_type='email',
                           expiry_time=int(time.time()),
                           is_active=True)

        user_otp.reset_expiry_time()


        response = super(TestCase02ResetUserPasswordV2APITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


