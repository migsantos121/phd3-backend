def get_user_action_entities(*args, **kwargs):
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
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    from ib_action.views.get_user_action_entities.utils.get_user_action_entities_response import \
        get_user_action_entities_response
    response_object = get_user_action_entities_response(request_data, user)

    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple = endpoint_response(response_object)

    return response_tuple
