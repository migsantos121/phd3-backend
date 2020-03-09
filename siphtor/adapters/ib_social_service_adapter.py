from ib_common.service_adapter_utils.base_adapter_class import BaseAdapterClass

__author__ = 'vedavidh'


class IBSocialServiceAdapter(BaseAdapterClass):
    def __init__(self, *args, **kwargs):
        from django.conf import settings
        self.request_type = settings.IB_SOCIAL_REQUEST_TYPE
        super(IBSocialServiceAdapter, self).__init__(*args, **kwargs)

    @property
    def conn(self):
        from ib_social.interfaces.CommonInterface import CommonInterface
        _interface = CommonInterface(self.user, self.access_token, self.request_type)
        return _interface

    def get_relations(self, m_id, m_type, relation_types, r_m_types):
        response = self.conn.get_relations(m_id, m_type, relation_types, r_m_types)
        return response

    def get_inverse_relations(self, r_m_id, r_m_type, relation_types, m_types):
        response = self.conn.get_inverse_relations(r_m_id, r_m_type, relation_types, m_types, status='ACCEPT')
        return response

    def get_relations_stats(self, request_data):
        response = self.conn.get_relations_stats(request_data)
        return response
