from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

from ib_users.models.ib_user import IBUser
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX

request_body = """
{
    "auth_type": "phone_number", 
    "username": "", 
    "country_code": "+91", 
    "client_id": "app_id", 
    "client_secret": "app_secret", 
    "password": "password123", 
    "phone_number": "1234567890", 
    "email": ""
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
from mock import mock


def get_oauth_details(user, client_id, client_secret, scopes='read write'):
    response = dict()
    tokens = dict()
    tokens['access_token'] = "apple"
    tokens['refresh_token'] = "ball"

    return ["apple", "ball"]


class TestCase01LoginUserV2APITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01LoginUserV2APITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX,
                                                               test_case,
                                                               *args, **kwargs)

    @mock.patch("ib_users.utilities.get_oauth_details.get_oauth_details", get_oauth_details)
    def test_case(self):
        from oauth2_provider.models import Application
        Application.objects.create(client_id='app_id', client_secret='app_secret', user_id=1)

        user = IBUser.objects.create(phone_number='1234567890',
                                     username='new_user',
                                     country_code='+91',
                                     dob='2012-02-02 12:21',
                                     is_phone_verified=True)
        user.set_password('password123')
        user.save()

        response = super(TestCase01LoginUserV2APITestCase, self).test_case()
        self.assertEqual(response.status_code, 200)
