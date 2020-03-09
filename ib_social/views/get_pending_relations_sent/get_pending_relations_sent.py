def get_pending_relations_sent(*args, **kwargs):
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
    request_data = kwargs['request_data']
    access_token = args[0].META["HTTP_AUTHORIZATION"].split(" ")[1]
    source = args[0].META.get('HTTP_X_SOURCE', '')
    from ib_social.views.get_pending_relations_sent.utils.get_pending_relations_sent_wrapper import \
        get_pending_relations_sent_wrapper
    response_object = get_pending_relations_sent_wrapper(request_data=request_data, user=user, source=source,
                                                         access_token=access_token)
    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple = endpoint_response(response_object)
    return response_tuple
