def get_actions_summary(*args, **kwargs):
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
    request_object = kwargs["request_object"]
    from ib_action.views.get_actions_summary.utils.get_actions_summary_response import get_actions_summary_response
    response_object = get_actions_summary_response(request_object,user)

    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple =  endpoint_response(response_object)

    return response_tuple
