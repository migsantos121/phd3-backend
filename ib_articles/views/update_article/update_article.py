from django.http.response import HttpResponse


def update_article(*args, **kwargs):
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

    from .api_wrapper import api_wrapper
    response_object = api_wrapper(*args, **kwargs)

    if response_object is None:
        from django.http.response import HttpResponse
        response_object = HttpResponse()

    # uncomment below lines for actual implementation when you have response_object / response_data
    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple = endpoint_response(response_object)

    return response_tuple
