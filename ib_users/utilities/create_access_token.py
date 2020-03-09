def create_access_token(user, application_id, scopes):
    import datetime
    from oauth2_provider.models import AccessToken
    from ib_users.utilities.generate_access_token import generate_access_token

    access_token = generate_access_token()
    expires = datetime.datetime.now() + datetime.timedelta(days=1000)
    access_token_object = AccessToken(user=user, token=access_token,
                                      application_id=application_id,
                                      expires=expires,
                                      scope=scopes)
    access_token_object.save()

    return access_token_object
