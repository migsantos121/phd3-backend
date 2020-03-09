from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase
from mock import mock

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

request_body = """
{
    "phone_number": "9160883374", 
    "auth_type": "phone_number", 
    "country_code": "91", 
    "client_id": "client_id", 
    "client_secret": "client_secret", 
    "email": "", 
    "verify_token": "123456"
}
"""

response_body = """
{
    "res_status": "Success", 
    "tokens": {
        "access_token": "waC5snR6QyAmgzc5lPkR7IAWznM28T", 
        "refresh_token": "waC5snR6QyAmgzc5lPkR7IAWznM28T"
    }, 
    "username": "username", 
    "user_id": 1
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


def generate_otp(username):
    return "123456"

def generate_access_token():

    return "waC5snR6QyAmgzc5lPkR7IAWznM28T"


class TestCase01UserLoginV2VerifyOtpAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01UserLoginV2VerifyOtpAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD,
                                                                        URL_SUFFIX, test_case,
                                                                        *args, **kwargs)


    @mock.patch("ib_users.utilities.generate_otp.generate_otp", generate_otp)
    @mock.patch("ib_users.utilities.generate_access_token.generate_access_token", generate_access_token)
    def test_case(self):

        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create(username="username", phone_number="9160883374", country_code="91",
                                   is_phone_verified=True)

        from ib_users.models.user_otp import UserOTP
        from ib_users.constants.user_reg_type import UserRegistrationType
        UserOTP.create_otp(user, UserRegistrationType.PHONE_NUMBER.value)

        from oauth2_provider.models import Application
        Application.objects.create(user=user, client_id="client_id", client_secret="client_secret")

        response = super(TestCase01UserLoginV2VerifyOtpAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)
