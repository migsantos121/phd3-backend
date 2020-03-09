from enum import Enum

__author__ = 'tanmay.ibhubs'


class UserRegistrationType(Enum):
    PHONE_NUMBER = "phone_number"
    EMAIL = "email"
    USERNAME = "username"
    EMAIL_AND_PHONE_NUMBER = "email_and_phone_number"

