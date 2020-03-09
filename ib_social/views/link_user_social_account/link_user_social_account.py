def link_user_social_account(*args, **kwargs):
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
    access_token = args[0].META.get("HTTP_AUTHORIZATION", 'Bearer  ').split(" ")[1]
    source = args[0].META.get('HTTP_X_SOURCE', '')

    print 'source--->', source

    user= kwargs['user']
    request_data = kwargs['request_data']
    from ib_social.models import MemberRelation
    response_object = MemberRelation.link_social_user_with_ib_user(user=user, access_token=access_token, source=source,
                                                                   **request_data)

    # uncomment below lines for actual implementation when you have response_object / response_data
    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple = endpoint_response(response_object)
    return response_tuple
