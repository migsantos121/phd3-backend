# coding=utf-8
import importlib
import json


def check_use_case(default_test_case, kwargs, app_name, operation_name):
    from django.conf import settings
    base_dir = settings.BASE_DIR
    tests_dir_path = base_dir + "/" + app_name + "/views/" + operation_name + "/tests/"
    from django_swagger_utils.drf_server.utils.server_gen.get_test_cases_dict import get_test_cases_dict
    test_cases_dict = get_test_cases_dict(tests_dir_path, operation_name)
    for test_case, test_case_dict in test_cases_dict.iteritems():
        try:
            import_str = "%s.views.%s.tests.%s" % (app_name, operation_name, test_case)
            test_case_data = getattr(importlib.import_module(import_str), "test_case")
            test_case_request_data = test_case_data["request"]
            request_body = test_case_request_data["body"]
            try:
                request_body = json.loads(request_body)
            except ValueError, err:
                request_body = None

            if not kwargs["request_query_params"]:
                kwargs["request_query_params"] = {}
            if not kwargs["request_headers_obj"]:
                kwargs["request_headers_obj"] = {}

            if request_body == kwargs["request_data"] and \
                    test_case_request_data["query_params"] == kwargs["request_query_params"] and \
                    test_case_request_data["header_params"] == kwargs["request_headers_obj"]:
                path_params_count = 0
                for path_param, path_param_value in test_case_request_data["path_params"].iteritems():
                    if kwargs.get(path_param) == path_param_value:
                        path_params_count += 1
                if len(test_case_request_data["path_params"]) == path_params_count:
                    default_test_case = test_case_data
                    break
        except (ImportError, AttributeError):
            pass
    return default_test_case
