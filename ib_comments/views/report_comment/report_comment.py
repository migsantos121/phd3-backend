def report_comment(*args, **kwargs):
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

    from django.http import HttpResponse
    req_user = kwargs["user"]
    req_obj = kwargs["request_object"]
    from ib_comments.views.report_comment.utils.report_comment_response import report_comment_response
    response_object = report_comment_response(req_obj, req_user)
    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    if response_object is None:

        response_object = HttpResponse()
        response_tuple = endpoint_response(response_object)
    else:
        response_tuple = endpoint_response(response_object, response_status_code=400)

    return response_tuple
