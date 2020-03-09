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
  "phone_number": "1234567890",
  "verify_token": "123456",
  "client_id": "app_id",
  "client_secret": "app_secret"
}
"""

response_body = """
{"tokens": {"access_token": "apple", "refresh_token": "ball"}, "res_status": "Success", "username": "new_user"}
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

    def __init__(self, *args, **kwargs):
        pass

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


def get_oauth_details(user, client_id, client_secret, scopes='read write'):
    print "i am here"
    response = dict()
    tokens = dict()
    tokens['access_token'] = "apple"
    tokens['refresh_token'] = "ball"

    return ["apple", "ball"]


class TestCase02VerifyDataUpdatePreLoginV2APITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase02VerifyDataUpdatePreLoginV2APITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD,
                                                                              URL_SUFFIX, test_case,
                                                                              *args, **kwargs)

    @mock.patch('ib_users.models.user_otp.UserOTP', UserOTP)
    @mock.patch("ib_users.utilities.get_oauth_details.get_oauth_details", get_oauth_details)
    def test_case(self):
        from oauth2_provider.models import Application
        Application.objects.create(client_id='app_id', client_secret='app_secret', user_id=1)

        user = IBUser.objects.create(phone_number='1234567890',
                                     username='new_user',
                                     country_code='+91',
                                     dob='2012-02-02 12:21',
                                     email='user@email.com',
                                     is_email_verified=False)
        user.set_password('password123')
        user.save()

        user_otp = UserOTP(ib_user=user,
                           otp_token=hash_otp('123456'),
                           auth_type='email',
                           expiry_time=int(time.time()),
                           is_active=True)

        user_otp.reset_expiry_time()
        response = super(TestCase02VerifyDataUpdatePreLoginV2APITestCase, self).test_case()
        self.assertEqual(response.status_code, 200)
