from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

request_body = """
{
    "client_secret": "client_secret", 
    "client_id": "client_id", 
    "social_provider_token": "access_token", 
    "provider": "twitter"
}
"""

response_body = """
{"tokens": {"access_token": "apple", "refresh_token": "ball"}, "res_status": "Success", username="tanmay.b"}
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


def get_details_from_twitter(social_access_token):
    return {
        'username': 'tanmay.b',
        'email': 'tanmay@ibhubs.co',
        'phone_number': '9876543201',
        'country_code': '+91',
        'id': '109237901273'
    }


def get_oauth_details(user, client_id, client_secret, scopes='read write'):
    response = dict()
    tokens = dict()
    tokens['access_token'] = "apple"
    tokens['refresh_token'] = "ball"

    response['tokens'] = tokens
    return ['apple', 'ball']


def generate_user_name(username=None):
    return 'tanmay'

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


class TestCase01SocialLoginAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01SocialLoginAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX,
                                                               test_case,
                                                               *args, **kwargs)

    @mock.patch("ib_users.models.user_otp.UserOTP", UserOTP)
    @mock.patch("ib_users.utilities.generate_random_username.generate_user_name", generate_user_name)
    @mock.patch("ib_users.utilities.get_oauth_details.get_oauth_details", get_oauth_details)
    @mock.patch("ib_users.utilities.social_login_utility.get_details_from_twitter", get_details_from_twitter)
    def test_case(self):
        from oauth2_provider.models import Application
        Application.objects.create(client_id='client_id', client_secret='client_secret', user_id=1)

        response = super(TestCase01SocialLoginAPITestCase, self).test_case()
        self.assertEqual(response.status_code, 200)
