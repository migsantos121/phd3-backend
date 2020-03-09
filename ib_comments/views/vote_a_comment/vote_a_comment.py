def vote_a_comment(*args, **kwargs):
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
    access_token = args[0].META["HTTP_AUTHORIZATION"].split(" ")[1]
    source = args[0].META.get('HTTP_SOURCE', '')
    request_object = kwargs["request_object"]
    from ib_comments.views.vote_a_comment.utils.vote_a_comment_response import vote_a_comment_response
    response_object = vote_a_comment_response(request_object, user, access_token=access_token, source=source)
    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    if response_object.has_key("error_code"):
        response_tuple = endpoint_response(response_object, response_status_code=400)
    else:
        response_tuple = endpoint_response(response_object)
    return response_tuple
