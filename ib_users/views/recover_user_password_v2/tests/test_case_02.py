from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from ib_users.models.ib_user import IBUser
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

request_body = """
{
    "auth_type": "email", 
    "username": "", 
    "client_id": "", 
    "country_code": "+91", 
    "client_secret": "", 
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


from mock import mock


class TestCase02RecoverUserPasswordV2APITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase02RecoverUserPasswordV2APITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD,
                                                                         URL_SUFFIX, test_case,
                                                                         *args, **kwargs)

    @mock.patch("ib_users.models.user_otp.UserOTP", UserOTP)
    def test_case(self):
        user = IBUser.objects.create(phone_number='1234567890',
                                     username='new_user',
                                     country_code='+91',
                                     email='user@email.com',
                                     dob='2012-02-02 12:21',
                                     is_email_verified=True)

        user.set_password('password123')
        user.save()

        response = super(TestCase02RecoverUserPasswordV2APITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)
