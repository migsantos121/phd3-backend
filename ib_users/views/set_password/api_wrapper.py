def api_wrapper(*args, **kwargs):
    request_data = kwargs['request_data']
    user = kwargs['user']

    from ib_users.models import IBUser
    response_object = IBUser.set_user_password(user, request_data['password'])
    return response_object
