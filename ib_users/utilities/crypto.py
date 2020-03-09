import hashlib

__author__ = 'tanmay.ibhubs'


def hash_otp(otp):
    hash_object = hashlib.sha1(otp)
    hex_dig = hash_object.hexdigest()
    return hex_dig
