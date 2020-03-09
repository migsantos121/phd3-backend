__author__ = 'vedavidh'


class BaseAdapterClass(object):
    def __init__(self, user, access_token):
        self.user = user
        self.access_token = access_token
