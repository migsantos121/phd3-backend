

TESTS = """{% autoescape off %}import json

from rest_framework import status
from rest_framework.test import APITestCase

from django_swagger_utils.drf_server.utils.server_gen.custom_test_utils import CustomTestUtils


class {{ operation_id }}APITestCase(APITestCase, CustomTestUtils):
    def test_case(self):
        app_name = "{{app_name}}"
        operation_name = "{{operation_id}}"
        request_method = "{{request_method|lower}}"

        from django_swagger_utils.drf_server.utils.server_gen.get_use_cases_list import get_use_cases_list
        use_cases_list = get_use_cases_list(app_name, operation_name)
        for use_case in use_cases_list:
            data = use_case["request_json"] # json request body string
            wrapped_request_data = {"data": json.dumps(data), "clientKeyDetailsId": 1}

            path_parameters = use_case.get("path_parameters", {})
            url_suffix = "{{example_path_url}}".format(**path_parameters)
            url = '/api/%s/%s' % (app_name, url_suffix)

            query_parameters = use_case.get("query_parameters", {})
            request_method_function = getattr(self.client, request_method)

            response = request_method_function(url, wrapped_request_data, params=query_parameters, format='json')

            try:
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(json.dumps(response.data), use_case["response_json"])
            except AssertionError as err:
                print response, response.content
                raise

{% endautoescape %}
"""
