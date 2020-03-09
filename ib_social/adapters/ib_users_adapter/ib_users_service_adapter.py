from ib_social.adapters.base_adapter_class import BaseAdapterClass

__author__ = 'tanmay.ibhubs'

class IBUsersServiceAdapter(BaseAdapterClass):
    def __init__(self, *args, **kwargs):
        from django.conf import settings
        self.request_type = settings.IB_USERS_REQUEST_TYPE
        super(IBUsersServiceAdapter, self).__init__(*args, **kwargs)

    @property
    def user_details(self):
        from .user_details import UserDetails
        return UserDetails(user=self.user, access_token=self.access_token, request_type=self.request_type)
