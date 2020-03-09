def get_friends_list(*args, **kwargs):
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
    request_object = kwargs['request_object']
    access_token = args[0].META["HTTP_AUTHORIZATION"].split(" ")[1]
    source = args[0].META.get('HTTP_X_SOURCE', '')
    from ib_social.views.get_friends_list.utils.get_friends_list_response import get_friends_list_response
    response_object = get_friends_list_response(request_object=request_object, user=user, access_token=access_token,
                                                source=source)
    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple = endpoint_response(response_object)
    return response_tuple
