import importlib


def get_api_environment(app_name, operation_name):
    '''
    says whether mock response or implied response is expected
    :param app_name: name of app
    :param operation_name: op id
    :return: ENV_MOCK or ENV_IMPL
    '''
    try:
        import_str = "%s.views.%s" % (app_name, operation_name)
        api_environment = getattr(importlib.import_module(import_str), "API_ENVIRONMENT")
    #setting default as mock
    except (ImportError, AttributeError) as err:
        api_environment = "ENV_MOCK"
    return api_environment


def check_to_execute_mock_test_for_operation(app_name, operation_name):
    '''
    tells whether to execute mock test for a operation of not
    :param app_name: name of app
    :param operation_name: op id
    :return: true or false
    '''
    try:
        import_str = "%s.views.%s" % (app_name, operation_name)

        execute_mock_test = getattr(importlib.import_module(import_str), "EXECUTE_API_TEST_CASE")
    #default=True
    except (ImportError, AttributeError) as err:
        execute_mock_test = True
    return execute_mock_test


def check_to_execute_mock_tests_for_apps(app_name):
    '''
    tells whether to execute mock test for an entire app or not
    :param app_name: name of app
    :return: true or false
    '''
    try:
        import_str = "%s" % (app_name,)
        execute_mock_test = getattr(importlib.import_module(import_str), "EXECUTE_API_TEST_CASE")
    #setting default as True
    except (ImportError, AttributeError) as err:
        execute_mock_test = True
    return execute_mock_test
