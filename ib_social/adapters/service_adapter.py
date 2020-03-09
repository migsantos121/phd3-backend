from .base_adapter_class import BaseAdapterClass

__author__ = 'tanmay.ibhubs'


class ServiceAdapter(BaseAdapterClass):
    def __init__(self, *args, **kwargs):
        super(ServiceAdapter, self).__init__(*args, **kwargs)

    @property
    def ib_users(self):
        from .ib_users_adapter.ib_users_service_adapter import IBUsersServiceAdapter
        return IBUsersServiceAdapter(user=self.user, access_token=self.access_token)
