def get_oauth_details(user, client_id, client_secret, scopes):

    from ib_users.utilities.get_application_id import get_application_id
    from ib_users.utilities.create_access_token import create_access_token
    from ib_users.utilities.create_refresh_token import create_refresh_token

    application_id = get_application_id(client_id, client_secret)
    access_token_object = create_access_token(user, application_id, scopes)
    refresh_token_object = create_refresh_token(user, application_id, access_token_object)

    tokens = [access_token_object.token, refresh_token_object.token]

    return tokens
