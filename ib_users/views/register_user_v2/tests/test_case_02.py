from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

request_body = """
{
    "phone_number": "", 
    "username": "email_user", 
    "pic_thumbnail": "", 
    "gender": "M", 
    "pic": "", 
    "dob": "2012-02-02 12:21", 
    "reg_type": "email", 
    "country_code": "", 
    "password": "user1234", 
    "email": "user@email.com",
    "registration_source":"apple"

}
"""

response_body = """
{"username": "email_user", "user_id": 1}
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


class TestCase02RegisterUserV2APITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase02RegisterUserV2APITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX,
                                                                  test_case,
                                                                  *args, **kwargs)

    @mock.patch("ib_users.models.user_otp.UserOTP", UserOTP)
    def test_case(self):
        response = super(TestCase02RegisterUserV2APITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)
