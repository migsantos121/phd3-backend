def get_relations(*args, **kwargs):
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
    source = args[0].META.get('HTTP_X_SOURCE', '')
    request_object = kwargs['request_object']
    user = kwargs["user"]
    from ib_social.views.get_relations.utils.get_relations_response import get_relations_response
    response_object = get_relations_response(request_object=request_object, user=user, source=source)
    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple =  endpoint_response(response_object)
    return response_tuple
