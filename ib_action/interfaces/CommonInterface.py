import os

from django_swagger_utils.drf_server.decorators.handle_exceptions import handle_exceptions


class CommonInterface():
    def __init__(self, user, access_token, request_type, source=''):
        self.user = user
        self.source = source
        self.access_token = access_token
        self.request_type = request_type
        self.branch = os.environ.get('DJANGO_SETTINGS_MODULE').split('.')[2]
        self.base_url = self.get_url()

    def get_url(self):
        from django.conf import settings
        base_url = getattr(settings, 'IB_ACTIONS_APIGATEWAY_ENDPOINT', '')
        return base_url + 'api/ib_action/'

    @handle_exceptions()
    def add_action(self, source, action_value, entity_id, action_type, entity_type):
        request_data = dict([
            ('source', source),
            ('action_value', action_value),
            ('entity_id', entity_id),
            ('action_type', action_type),
            ('entity_type', entity_type),
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'action/'
            from ib_action.interfaces.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          user_data=request_data, source=self.source)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_action.views.add_action.utils.add_action_response import add_action_response
            return add_action_response(request_data, self.user, self.source, self.access_token)
        else:
            pass

    @handle_exceptions()
    def get_actions_summary(self, entity_id, entity_type, source, action_type_filters):
        request_data = dict([
            ('source', source),
            ('entity_id', entity_id),
            ('entity_type', entity_type),
            ('action_types', action_type_filters)
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'summary/'
            from ib_action.interfaces.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          user_data=request_data)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_action.views.get_actions_summary.utils.get_actions_summary_response import \
                get_actions_summary_response
            return get_actions_summary_response(request_data, self.user)
        else:
            pass

    @handle_exceptions()
    def get_users_actions_summaries(self, entities, source, user_ids, action_type_filters):
        request_data = dict([
            ('source', source),
            ('entities', entities),
            ('action_types', action_type_filters),
            ('user_ids', user_ids)
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'summary/users/'
            from ib_action.interfaces.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          user_data=request_data, source=self.source)
            return response_object
        elif self.request_type == 'LIBRARY':

            from ib_action.views.get_users_actions_summary.utils.get_users_actions_summary_response import \
                get_users_actions_summary_response
            return get_users_actions_summary_response(request_data, self.user)
        else:
            pass

    @handle_exceptions()
    def get_entities(self, source, user_ids, entity_type):
        request_data = dict([
            ('source', source),
            ('entity_type', entity_type),
            ('user_ids', user_ids)
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'entities/'
            from ib_action.interfaces.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          user_data=request_data)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_action.views.get_entities.utils.get_entities_response import get_entities_response
            return get_entities_response(request_data, self.user)
        else:
            pass

    @handle_exceptions()
    def get_user_action_entities(self, offset, limit, source, entity_type, action_type):
        request_data = dict([
            ('source', source),
            ('entity_type', entity_type),
            ('action_type', action_type),
            ('offset', offset),
            ('limit', limit),
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'users/actions/entities/'
            from ib_action.interfaces.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          user_data=request_data)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_action.views.get_user_action_entities.utils.get_user_action_entities_response import \
                get_user_action_entities_response
            return get_user_action_entities_response(request_data, self.user)
        else:
            pass

    @handle_exceptions()
    def get_user_actions_entities(self, offset, limit, source, entity_types, action_types, action_values):
        request_data = dict([
            ('source', source),
            ('entity_types', entity_types),
            ('action_types', action_types),
            ('action_values', action_values),
            ('offset', offset),
            ('limit', limit),
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'users/actions/entities/v2/'
            from ib_action.interfaces.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          user_data=request_data)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_action.views.get_user_actions_entities.api_wrapper import api_wrapper
            return api_wrapper(request_data=request_data, user=self.user)
        else:
            pass

    @handle_exceptions()
    def user_action_counts(self,source, entity_types, action_types, action_values):
        request_data = dict([
            ('source', source),
            ('entity_types', entity_types),
            ('action_types', action_types),
            ('action_values', action_values),
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/actions/counts/'
            from ib_action.interfaces.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          user_data=request_data)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_action.views.user_action_counts.api_wrapper import api_wrapper
            return api_wrapper(request_data=request_data, user=self.user)
        else:
            pass
