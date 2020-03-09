def get_oauth_details_response(user, client_id, client_secret, scopes='read write'):

    from ib_users.utilities.get_oauth_details import get_oauth_details
    oauth_details = get_oauth_details(user, client_id, client_secret, scopes)

    response = dict()
    tokens = dict()
    if oauth_details is None:
        response['tokens'] = dict()
        response['res_status'] = "Invalid Application"
    else:
        tokens['access_token'] = oauth_details[0]
        tokens['refresh_token'] = oauth_details[1]

        response['tokens'] = tokens
        response['res_status'] = "Success"

    response["username"] = user.username
    response["user_id"] = user.id
    return response
