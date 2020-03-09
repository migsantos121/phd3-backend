import json
import os

from django_swagger_utils.core.parsers.swagger_parser import SwaggerParser
from django_swagger_utils.core.utils.check_path_exists import check_path_exists
from django_swagger_utils.drf_server.utils.server_gen.get_api_environment import check_to_execute_mock_test_for_operation


def get_app_test_labels(base_dir, app_name):
    '''

    :param base_dir: your project directory
    :param app_name: app name
    :return: returns list of views for which mocktests are to be done
    '''
    app_dir=os.path.join(base_dir,app_name)
    views_dir = os.path.join(app_dir,"views")
    spec_file_path = os.path.join(os.path.join(app_dir, "api_specs"),"api_spec.json")
    if not spec_file_path:
        raise Exception(" %s/api_specs/api_spec.json missing" % app_name)
    with open(spec_file_path) as f:
        spec_file_contents = f.read()
        try:
            spec_json = json.loads(spec_file_contents)
        except ValueError:
            print "The \"%s/api_specs/api_spec.json\" is not a proper JSON." % app_name
            exit(1)

    parser = SwaggerParser(spec_json=spec_json)
    #TODO code duplicacy apidoc and here
    op_of_last_version = []

    with open(base_dir + "/" + app_name + "/api_specs/api_spec.json") as src_json:
        src = json.load(src_json)
    for path_name, path in parser.paths().iteritems():

        for method, method_props in path.iteritems():
            # Handle common parameters later

            if (method == 'get') or (method == 'post') or (method == 'delete') or (method == 'put'):
                operation_id = method_props.get("operationId")
                op_of_last_version.append(operation_id)

    #make a list of views to be subjected to mocktest
    req_endpoints = []
    for endpoint_name in os.listdir(views_dir):
        if os.path.isdir(os.path.join(views_dir, endpoint_name)):
            #the below function call will return a bool,if its true add it to list
            execute_mock_test = check_to_execute_mock_test_for_operation(app_name, endpoint_name)
            if execute_mock_test == True:
                req_endpoints.append(endpoint_name)
    dir_list = []
    #adding tests path to the list
    for endpoint_name in req_endpoints:
        if endpoint_name in op_of_last_version:
            #the reason this is not written using os.apth.join() is django import statements support
            #dots to join files not '/'
            tests_path_for_import=app_name+".views."+endpoint_name+".tests"
            test_case_init_path=os.path.join(os.path.join(os.path.join(views_dir , endpoint_name ), "tests"), "__init__.py")
            test_path = check_path_exists(test_case_init_path)
            if test_path:
                dir_list.append(tests_path_for_import)
    #if nothing is added that means all tests are marked to false , terminate the programs giving a message
    if len(dir_list) == 0:
        print "all mock tests marked false,no tests to run "
        print "please change execute mock test to true wherever required"
        exit(1)

    return dir_list
