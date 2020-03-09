def verify_data_update_v2(*args, **kwargs):
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
    request_data = kwargs["request_data"]
    user = kwargs['user']
    from ib_users.models import IBUser
    auth_type = request_data['auth_type']
    country_code = request_data.get('country_code', None)
    phone_number = request_data.get('phone_number', None)
    email = request_data.get('email', None)
    verify_token = request_data.get('verify_token', None)

    response_object = IBUser.verify_user_data_update_v2(auth_type=auth_type, phone_number=phone_number,
                                                        country_code=country_code, email=email,
                                                        verify_token=verify_token, user=user)

    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple = endpoint_response(response_object)

    return response_tuple
