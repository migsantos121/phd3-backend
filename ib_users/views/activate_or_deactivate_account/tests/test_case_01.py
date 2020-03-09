from ib_users.models.ib_user import IBUser
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "make_active": false
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
        "securities": {"oauth": {"scopes": ["write"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01ActivateOrDeactivateAccountAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01ActivateOrDeactivateAccountAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        user = IBUser.objects.create(phone_number='1234567890',
                                     username='new_user',
                                     country_code='+91',
                                     email='user@email.com',
                                     dob='2012-02-02 12:21',
                                     is_phone_verified=True)

        user.set_password('password123')

        response = super(TestCase01ActivateOrDeactivateAccountAPITestCase, self).test_case()
        self.assertEqual(response.status_code, 200)

    def setupUser(self, username, password):
        super(TestCase01ActivateOrDeactivateAccountAPITestCase, self).setupUser(username, password)

        self.foo_user.first_name = "user"
        self.foo_user.save()



