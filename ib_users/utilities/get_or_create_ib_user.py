def get_or_create_ib_user(username, country_code, registration_source):
    from ib_users.models.ib_user import IBUser
    from ib_users.models.otp_details import OTPDetails
    from ib_users.models.registration_source import RegistrationSource
    from ib_users.utilities.check_username import check_username

    if check_username(username):
        new_country_code = country_code
    else:
        new_country_code = "-1"

    try:
        ib_user = IBUser.objects.get(username=username)
    except IBUser.DoesNotExist:
        ib_user = IBUser.objects.create(username=username, country_code=new_country_code, status="REGISTERED")
        OTPDetails.objects.create(ib_user=ib_user, otp_count=0)

    try:
        reg_source = RegistrationSource.objects.get(registration_source=registration_source)
    except RegistrationSource.DoesNotExist:
        reg_source = RegistrationSource.objects.create(registration_source=registration_source)

    from ib_users.models import IBUserRegistrationSource
    IBUserRegistrationSource.create_user_registration_source(ib_user, reg_source)

    return ib_user
