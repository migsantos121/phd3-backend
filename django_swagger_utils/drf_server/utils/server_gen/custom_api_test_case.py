import base64
import json
import urllib
import logging

from rest_framework.test import APITestCase

from django_swagger_utils.drf_server.utils.server_gen.custom_test_utils import CustomTestUtils

logger = logging.getLogger(__name__)


class CustomAPITestCase(APITestCase, CustomTestUtils):
    def __init__(self, app_name, operation_name, request_method, url_suffix, test_case_dict, *args, **kwargs):
        super(CustomAPITestCase, self).__init__(*args, **kwargs)
        self.app_name = app_name
        self.operation_name = operation_name
        self.request_method = request_method
        self.url_suffix = url_suffix
        self.url = kwargs.get("url")
        self.test_case_dict = test_case_dict

    def setupUser(self, username, password):
        self.foo_user = self._create_user(username, password)

    def setupOAuth(self, scopes):
        self.app_foo = self._create_application('app foo_user 1', self.foo_user)
        self.foo_access_token = self._get_access_token(user=self.foo_user, app=self.app_foo, scope=scopes)
        self.mock_auth(self.client, self.foo_access_token.token)

    def test_case(self):
        test_case_request_dict = self.test_case_dict["request"]

        header_parameters = test_case_request_dict.get("header_params", {})
        path_parameters = test_case_request_dict.get("path_params", {})
        if self.url:
            url = self.url.format(**path_parameters)
        else:
            url_suffix = self.url_suffix.format(**path_parameters)
            url = '/api/%s/%s' % (self.app_name, url_suffix)

        query_parameters = test_case_request_dict.get("query_params", {})
        request_method_function = getattr(self.client, self.request_method)

        securities = test_case_request_dict["securities"]

        # todo request content type
        # todo response content type

        oauth_scopes = []
        username = None
        password = None
        for security, security_def in securities.iteritems():
            if security_def["type"] == "oauth2":
                oauth_scopes.extend(security_def["scopes"])
            elif security_def["type"] == "apiKey":
                if security_def["in"] == "header":
                    header_parameters.update({security_def["header_name"]: security_def["value"]})
                else:
                    query_parameters.update({security_def["name"]: security_def["value"]})
            elif security_def["type"] == "basic":
                auth_value = 'Basic ' + base64.b64encode('%s:%s' % (security_def["username"], security_def["password"]))
                header_parameters.update({"HTTP_AUTHORIZATION": auth_value})
                username = security_def["username"]
                password = security_def["password"]
        if oauth_scopes:
            oauth_scopes = " ".join(oauth_scopes)
            username = "username"
            password = "password"
        if username:
            self.setupUser(username=username, password=password)
        if oauth_scopes:
            self.setupOAuth(oauth_scopes)

        test_case_request_dict = self.test_case_dict["request"]
        data = test_case_request_dict["body"]  # json request body string

        test_case_response_dict = self.test_case_dict["response"]
        if query_parameters:
            url += "?" + urllib.urlencode(query_parameters, doseq=True)
        if self.request_method == "get":
            wrapped_request_data = query_parameters
        else:
            from django.conf import settings
            django_swagger_utils_settings = settings.SWAGGER_UTILS
            defaults = django_swagger_utils_settings["DEFAULTS"]
            if defaults.get("REQUEST_WRAPPING_REQUIRED", True):
                wrapped_request_data = {"data": json.dumps(data), "clientKeyDetailsId": 1}
            else:
                wrapped_request_data = json.loads(data)

        print header_parameters
        response = request_method_function(url, wrapped_request_data, format='json', **header_parameters)

        try:
            print "Response Content:"
            print response.content
            self.assertEqual(response.status_code, test_case_response_dict["status"])
            try:
                test_case_response = json.loads(test_case_response_dict["body"])
                test_response = json.loads(response.content)
                self.assertEqual(test_response, test_case_response)
            except ValueError, err:
                logger.info(err)

                test_response = response.content
                if test_response:
                    test_response = test_response.strip()
                test_case_response = test_case_response_dict["body"].strip()
                print test_case_response, test_response
                self.assertEqual(test_response, test_case_response)

                pass

            test_response_headers = test_case_response_dict["header_params"]
            for header_name, header_val in test_response_headers.iteritems():
                header_name = header_name.replace("_", "-")
                response_header = response._headers.get(header_name)
                self.assertEqual(response_header[1], header_val)

        except AssertionError as err:
            print response, response.content
            raise
        print "=============================================="
        print self.operation_name
        print response
        print "==============================================\n\n\n"
        return response

    def tearDown(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        from oauth2_provider.models import Application
        User.objects.all().delete()
        Application.objects.all().delete()
