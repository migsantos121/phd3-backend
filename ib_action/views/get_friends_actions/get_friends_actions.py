def get_friends_actions(*args, **kwargs):
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
    access_token = args[0].META["HTTP_AUTHORIZATION"].split(" ")[1]
    from ib_action.views.get_friends_actions.utils.get_friends_actions_response import get_friends_actions_response
    response_object = get_friends_actions_response(request_data=request_data, user=user, access_token=access_token)
    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple =  endpoint_response(response_object)
    return response_tuple