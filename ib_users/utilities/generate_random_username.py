__author__ = 'tanmay.ibhubs'
from django.utils.crypto import get_random_string


def generate_user_name(username=None):
    if username is not None:
        username = username.replace(' ', '_')
        return username + "_" + get_random_string()
    else:
        return get_random_string(30)
