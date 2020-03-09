TEST_CASE = """{% autoescape off %}from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = \"\"\"
{{request_body_sample_json}}
\"\"\"

response_body = \"\"\"
{{responses.200.response_serializer_sample_json}}
\"\"\"

\"\"\"
Write your test case description here
\"\"\"

test_case = {
    "request": {
        "path_params": {{path_params}},
        "query_params": {{request_query_params}},
        "header_params": {{request_headers_params}},
        "securities": {{securities}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {{responses.200.response_headers_example_params}}
    }
}


class {{test_case_class}}(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super({{test_case_class}}, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super({{test_case_class}}, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)

{% endautoescape %}
"""
