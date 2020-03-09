def get_social_details(*args, **kwargs):
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
    request_data = kwargs['request_data']
    user = kwargs['user']
    social_ids = request_data.get('social_ids', [])
    social_provider = request_data.get('social_provider', None)
    from ib_users.models.user_social_provider import UserSocialProvider
    response_object = UserSocialProvider.get_users_from_social_ids(social_ids, social_provider)

    # uncomment below lines for actual implementation when you have response_object / response_data
    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple =  endpoint_response(response_object)

    return response_tuple
