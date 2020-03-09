from ib_common.service_adapter_utils.base_adapter_class import BaseAdapterClass

__author__ = 'vedavidh'


class IBCommentsServiceAdapter(BaseAdapterClass):
    def __init__(self, *args, **kwargs):
        from django.conf import settings
        self.request_type = settings.IB_COMMENTS_REQUEST_TYPE
        super(IBCommentsServiceAdapter, self).__init__(*args, **kwargs)

    @property
    def conn(self):
        from ib_comments.interfaces.CommonInterface import CommonInterface
        _interface = CommonInterface(self.user, self.access_token, self.request_type)
        return _interface

    def get_count_of_comments(self, entities):
        response = self.conn.get_count_of_comments(entities)
        return response




