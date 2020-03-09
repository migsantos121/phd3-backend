def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    req_data = kwargs['request_data']
    old_password = req_data['old_password']
    new_password = req_data['new_password']

    from ib_users.models.ib_user import IBUser
    response_object = IBUser.update_password(user, old_password, new_password)
    return response_object
