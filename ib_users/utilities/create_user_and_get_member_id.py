def create_user_and_get_member_id(source, username, name, pic, dob):
    from ib_users.models.ib_user import IBUser
    from ib_users.models.registration_source import RegistrationSource
    from datetime import datetime
    if dob is not None:
        dob = datetime.strptime(dob, '%Y-%m-%d')
    else:
        dob = None

    try:
        user = IBUser.objects.get(username=username)
        if user.pic is None:
            user.pic = pic
            user.save()

    except IBUser.DoesNotExist:
        if dob is not None:
            user = IBUser.objects.create(username=username, name=name, pic=pic, status="NOT_REGISTERED",
                                         country_code=-1, dob=dob)
        else:
            user = IBUser.objects.create(username=username, name=name, pic=pic, status="NOT_REGISTERED",
                                         country_code=-1)

    try:
        reg_source = RegistrationSource.objects.get(registration_source=source)
    except RegistrationSource.DoesNotExist:
        reg_source = RegistrationSource.objects.create(registration_source=source)

    from ib_users.models import IBUserRegistrationSource
    IBUserRegistrationSource.create_user_registration_source(user, reg_source)

    return user
