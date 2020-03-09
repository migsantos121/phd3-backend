from ib_common.service_adapter_utils.base_adapter_class import BaseAdapterClass

__author__ = 'vedavidh'


class IBActionsServiceAdapter(BaseAdapterClass):
    def __init__(self, *args, **kwargs):
        from django.conf import settings
        self.request_type = settings.IB_ACTIONS_REQUEST_TYPE
        super(IBActionsServiceAdapter, self).__init__(*args, **kwargs)

    @property
    def conn(self):
        from ib_action.interfaces.CommonInterface import CommonInterface
        _interface = CommonInterface(self.user, self.access_token, self.request_type)
        return _interface

    def get_users_actions_summaries(self, entities, source, user_ids, action_type_filters):
        response = self.conn.get_users_actions_summaries(entities, source, user_ids, action_type_filters)
        return response

    def get_user_actions_entities(self, offset, limit, source, entity_types, action_types, action_values):
        response = self.conn.get_user_actions_entities(offset, limit, source, entity_types, action_types, action_values)
        return response

    def user_action_counts(self, source, entity_types, action_types, action_values):
        response = self.conn.user_action_counts(source, entity_types, action_types, action_values)
        return response
