def create_refresh_token(user, application_id, access_token_object):
    from oauth2_provider.models import RefreshToken
    from ib_users.utilities.generate_access_token import generate_access_token

    refresh_token = generate_access_token()
    refresh_token_object = RefreshToken(user=user, token=refresh_token, application_id=application_id,
                                        access_token=access_token_object)
    refresh_token_object.save()

    return refresh_token_object
