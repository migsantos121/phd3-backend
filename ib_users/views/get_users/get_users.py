def get_users(*args, **kwargs):
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
    # from ib_users.views.get_users.tests.test_case_01 import test_case
    # from django_swagger_utils.drf_server.utils.server_gen.mock_response import mock_response
    # response_tuple = mock_response(app_name="ib_users", operation_name="get_users", test_case=test_case,
    #                                kwargs=kwargs)
    # end of mock view implementation

    req_data = kwargs["request_data"]
    user_ids = req_data['user_ids']
    source = args[0].META.get('HTTP_X_SOURCE', '')
    search_q = req_data.get("search_q", "")
    exclude_user_ids = req_data.get("exclude_user_ids", [])
    offset = req_data.get('offset', None)
    limit = req_data.get('limit', None)
    print 'User Ids--->', user_ids

    from ib_users.models.ib_user import IBUser
    response_object = IBUser.get_member_details_by_id(user_ids=user_ids, search_q=search_q,
                                                      exclude_user_ids=exclude_user_ids, source=source,
                                                      offset=offset, limit=limit)

    # uncomment below lines for actual implementation when you have response_object / response_data
    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple = endpoint_response(response_object)

    return response_tuple
