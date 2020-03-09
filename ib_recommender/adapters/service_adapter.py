from ib_common.service_adapter_utils.base_adapter_class import BaseAdapterClass

__author__ = 'vedavidh'


class ServiceAdapter(BaseAdapterClass):
    def __init__(self, *args, **kwargs):
        super(ServiceAdapter, self).__init__(*args, **kwargs)

    @property
    def ib_articles(self):
        from .ib_articles_service_adapter import IBArticlesServiceAdapter
        return IBArticlesServiceAdapter(access_token=self.access_token, user=self.user)
