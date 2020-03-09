import json

from django.http import HttpResponse


def mock_response(app_name, operation_name, test_case, kwargs):
    from django_swagger_utils.drf_server.utils.server_gen.check_use_case import check_use_case
    test_case = check_use_case(test_case, kwargs, app_name, operation_name)
    response_data = test_case["response"]
    content = response_data["body"]
    status = response_data["status"]

    try:
        if isinstance(content, dict) or isinstance(content, list):
            content = json.dumps(content, indent=4)
        response = json.loads(content)
    except Exception, err:
        response = HttpResponse(content=content, status=status)
    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    return endpoint_response(response, response_data["status"], response_data["header_params"])
