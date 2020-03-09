"""
Created on 14/06/17

@author: revanth
"""


def populate_user_with_email(email, reg_source):
    from ib_users.models import IBUser
    try:
        user = IBUser.objects.get(email=email)
        print user.name, user.id, ' already exists'
        return
    except:
        pass

    from django.utils.crypto import get_random_string
    username = get_random_string(30)

    name = email.split('@')[0]
    if '.' in name:
        first_name = name.split('.')[0].title()
        last_name = name.split('.')[1].title()
    else:
        first_name = name.title()
        last_name = ''

    name = first_name+' ' + last_name
    password = first_name+'@123'

    from ib_users.models import IBUser
    user = IBUser(username=username)
    user.first_name = first_name
    user.last_name = last_name
    user.name = name
    user.set_password(password)
    user.email = email
    user.is_email_verified = True
    user.save()

    print user.name, user.id, ' created successfully'

    from ib_users.models import RegistrationSource, IBUserRegistrationSource
    registration_source_obj, is_created = RegistrationSource.objects.get_or_create(
        registration_source=reg_source)
    IBUserRegistrationSource.create_user_registration_source(user, registration_source_obj)
    return
