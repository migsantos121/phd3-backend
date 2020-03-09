from django.http import HttpResponse, response
def twitter_request(request, *args, **kwargs):
    """
    Note: replace below mock implementation with your actual implementation

    Request:

    kwargs["user"]                  -> request user
    kwargs["request_object"]        -> request body type object
    kwargs["request_data"]          -> request body data dict
    kwargs["request_headers_obj"]   -> request headers object
    kwargs["request_query_params"]  -> request query parameters object

    Response :

    return: tuple(response_status_code, response_object,
                  response_headers_object)

    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response \
            import endpoint_response
    return endpoint_response(response_object)

    """
    from ib_users.models import twitter
    response_object = twitter.twitter_request(request)

    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple = endpoint_response(response_object)
    return response_tuple
