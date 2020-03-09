def update_relation(*args, **kwargs):
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
    request_object = kwargs['request_object']
    access_token = args[0].META["HTTP_AUTHORIZATION"].split(" ")[1]
    source = args[0].META.get('HTTP_X_SOURCE', '')
    user = kwargs["user"]
    from ib_social.views.update_relation.utils.update_relation_response import update_relation_response
    response_object = update_relation_response(request_object, user, access_token, source)
    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple =  endpoint_response(response_object)
    return response_tuple
