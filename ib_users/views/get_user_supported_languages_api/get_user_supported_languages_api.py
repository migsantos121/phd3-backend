def get_user_supported_languages_api(*args, **kwargs):
    """
    Note: replace below mock implementation with your actual implementation

    Request:

    kwargs["user"]                  -> request user
    kwargs["request_object"]        -> request body type object
    kwargs["request_data"]          -> request body data dict
    kwargs["request_headers_obj"]   -> request headers object
    kwargs["request_query_params"]  -> request query parameters object

    Response :

    return: tuple(response_status_code, response_object, response_headers_object)

    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    return endpoint_response(response_object)

    """
    # mock response implementation starts
    # from ib_users.views.get_user_supported_languages_api.tests.test_case_01 import test_case
    # from django_swagger_utils.drf_server.utils.server_gen.mock_response import mock_response
    # response_tuple = mock_response(app_name="ib_users", operation_name="get_user_supported_languages_api", test_case=test_case,
    #                                kwargs=kwargs)
    # end of mock view implementation
    source = args[0].META.get('HTTP_X_SOURCE', '')
    kwargs['source'] = source
    request_data = kwargs['request_data']

    from .get_user_supported_languages_api_wrapper import get_user_supported_languages_api_wrapper
    response_object = get_user_supported_languages_api_wrapper(request_data)
    # uncomment below lines for actual implementation when you have response_object / response_data
    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple =  endpoint_response(response_object)

    return response_tuple
