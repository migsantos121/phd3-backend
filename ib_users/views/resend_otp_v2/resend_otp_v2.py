def resend_otp_v2(*args, **kwargs):
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
    req_data = kwargs['request_data']
    username = req_data.get('username', None)
    email = req_data.get('email', None)
    phone_number = req_data.get('phone_number', None)
    country_code = req_data.get('country_code', None)
    auth_type = req_data['auth_type']
    client_id = req_data['client_id']
    client_secret = req_data['client_secret']

    from ib_users.models.ib_user import IBUser
    response_object = IBUser.resend_otp_v2(username, auth_type, phone_number, country_code, email, client_id,
                                           client_secret)
    # uncomment below lines for actual implementation when you have response_object / response_data
    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple = endpoint_response(response_object)

    return response_tuple
