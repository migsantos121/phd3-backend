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
        base_url = getattr(settings, 'IB_SOCIAL_APIGATEWAY_ENDPOINT', '')
        return base_url + 'api/ib_social/'

    @handle_exceptions()
    def update_relation(self, m_id, m_type, r_m_id, r_m_type, relation):
        request_data = dict([
            ('m_id', m_id),
            ('m_type', m_type),
            ('r_m_id', r_m_id),
            ('r_m_type', r_m_type),
            ('relation', relation)
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'member/update_relation/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token, source=self.source,
                                          request_data=request_data, client_key_details_id=1, request_type="POST")
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_social.views.update_relation.utils.update_relation_response import update_relation_response
            return update_relation_response(request_data, self.user, self.access_token, self.source)
        else:
            pass

    @handle_exceptions()
    def update_relation_status(self, m_id, m_type, r_m_id, r_m_type, relation, status):
        request_data = dict([
            ('m_id', m_id),
            ('m_type', m_type),
            ('r_m_id', r_m_id),
            ('r_m_type', r_m_type),
            ('relation', relation),
            ('status', status)
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'member/update_relation_status/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, request_type="POST")
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_social.views.update_relation_status.utils.update_relation_status_response import \
                update_relation_status_response
            return update_relation_status_response(request_data, self.user, self.access_token, self.source)
        else:
            pass

    @handle_exceptions()
    def get_relations(self, m_id, m_type, relation_types, r_m_types):
        request_data = dict([
            ('m_id', m_id),
            ('m_type', m_type),
            ('relation_types', relation_types),
            ('r_m_types', r_m_types)
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'member/get_relations/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token, source=self.source,
                                          request_data=request_data, client_key_details_id=1, request_type="POST")
            return response_object
        elif self.request_type == 'LIBRARY':

            from ib_social.views.get_relations.utils.get_relations_response import get_relations_response
            return get_relations_response(request_data, self.user, self.source)
        else:
            pass

    @handle_exceptions()
    def get_inverse_relations(self, r_m_id, r_m_type, relation_types, m_types, status):
        request_data = dict([
            ('r_m_id', r_m_id),
            ('r_m_type', r_m_type),
            ('relation_types', relation_types),
            ('m_types', m_types),
            ('status', status)
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'member/get_inverse_relations/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token, source=self.source,
                                          request_data=request_data, client_key_details_id=1, request_type="POST")
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_social.views.get_inverse_relations.api_wrapper import api_wrapper
            return api_wrapper(request_data=request_data, user=self.user, source=self.source)
        else:
            pass

    @handle_exceptions()
    def verify_relations(self, request_data):
        if self.request_type == 'SERVICE':
            url = self.base_url + 'member/verify_relations/'
            from ib_common.utilities.api_request import api_request
            print url, self.access_token, request_data
            response_object = api_request(base_url=url, access_token=self.access_token, source=self.source,
                                          request_data=request_data, client_key_details_id=1, request_type="POST")
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_social.views.verify_relations.utils.verify_relations_response import verify_relations_response
            return verify_relations_response(request_data, self.user, source=self.source, )
        else:
            pass

    @handle_exceptions()
    def get_relations_stats(self, request_data):
        if self.request_type == 'SERVICE':
            url = self.base_url + 'relations/stats/'
            from ib_common.utilities.api_request import api_request
            print url, self.access_token, request_data
            response_object = api_request(base_url=url, access_token=self.access_token, source=self.source,
                                          request_data=request_data, client_key_details_id=1, request_type="POST")
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_social.views.get_relations_stats.api_wrapper import api_wrapper
            return api_wrapper(request_data=request_data, user=self.user, source=self.source)
        else:
            pass

    @handle_exceptions()
    def friends_with_relation(self, r_m_id, r_m_type, limit, offset, relation):
        request_data = dict([
            ('r_m_id', r_m_id),
            ('limit', limit),
            ('offset', offset),
            ('r_m_type', r_m_type),
            ('relation', relation)
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'friends_with_relation/'
            from ib_common.utilities.api_request import api_request
            print url, self.access_token, request_data
            response_object = api_request(base_url=url, access_token=self.access_token, source=self.source,
                                          request_data=request_data, client_key_details_id=1, request_type="POST")
            return response_object
        elif self.request_type == 'LIBRARY':

            from ib_social.views.friends_with_relation.utils.friends_with_relation_response import \
                friends_with_relation_response
            return friends_with_relation_response(request_data, self.user, access_token=self.access_token,
                                                  source=self.source)
        else:
            pass

    @handle_exceptions()
    def get_friends_list(self, m_id, m_type, limit, offset, search_q, source="com.vi"):
        request_data = dict([
            ('m_id', m_id),
            ('limit', limit),
            ('offset', offset),
            ('m_type', m_type),
            ('search_q', search_q)
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'member/get_friends_list/'
            from ib_common.utilities.api_request import api_request
            print url, self.access_token, request_data
            response_object = api_request(base_url=url, access_token=self.access_token, source=self.source,
                                          request_data=request_data, client_key_details_id=1, request_type="POST")
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_social.views.get_friends_list.utils.get_friends_list_response import get_friends_list_response
            return get_friends_list_response(request_data, self.user, access_token=self.access_token, source=source)
        else:
            pass

    @handle_exceptions()
    def get_friends_list_bulk(self, request_data):
        if self.request_type == 'SERVICE':
            url = self.base_url + 'member/get_friends_list/bulk/'
            from ib_common.utilities.api_request import api_request
            print url, self.access_token, request_data
            response_object = api_request(base_url=url, access_token=self.access_token, source=self.source,
                                          request_data=request_data, client_key_details_id=1, request_type="POST")
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_social.views.get_friends_list_bulk.utils.get_friends_list_bulk_response import \
                get_friends_list_bulk_response
            return get_friends_list_bulk_response(request_data, self.user, access_token=self.access_token,
                                                  source=self.source, )
        else:
            pass

    @handle_exceptions()
    def link_user_social_account(self, social_provider=None, social_token=None, social_access_token_secret=None,
                                 source=''):
        request_data = {
            "social_provider": social_provider,
            "social_token": social_token,
            "social_access_token_secret": social_access_token_secret
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/link_social_account/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token, source=self.source,
                                          request_data=request_data, client_key_details_id=1, request_type="POST")
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_social.models.member_relation import MemberRelation
            return MemberRelation.link_social_user_with_ib_user(user=self.user, access_token=self.access_token,
                                                                social_token=social_token,
                                                                social_access_token_secret=social_access_token_secret,
                                                                social_provider=social_provider, source=source)
        else:
            pass

    @handle_exceptions()
    def delink_user_social_account(self, social_provider=None, source=''):
        request_data = {
            'social_provider': social_provider
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/delink_social_account/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token, source=self.source,
                                          request_data=request_data, client_key_details_id=1, request_type="POST")
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_social.models.member_relation import MemberRelation
            return MemberRelation.delink_user_social_account(user=self.user, social_provider=social_provider,
                                                             access_token=self.access_token, source=source)
        else:
            pass

    @handle_exceptions()
    def get_pending_relation_sent(self, m_id, m_type, offset, limit, relation_types):
        request_data = {
            "m_id": m_id,
            "m_type": m_type,
            "offset": offset,
            "limit": limit,
            "relation_types": relation_types
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'member/get_pending_relations_sent/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token, source=self.source,
                                          request_data=request_data, client_key_details_id=1, request_type="POST")
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_social.views.get_pending_relations_sent.utils.get_pending_relations_sent_wrapper import \
                get_pending_relations_sent_wrapper
            return get_pending_relations_sent_wrapper(request_data=request_data, user=self.user,
                                                      access_token=self.access_token, source=self.source)
        else:
            pass

    @handle_exceptions()
    def get_pending_relation_requests(self, m_id, m_type, offset, limit, relation_types):
        request_data = {
            "m_id": m_id,
            "m_type": m_type,
            "offset": offset,
            "limit": limit,
            "relation_types": relation_types
        }

        if self.request_type == 'SERVICE':
            url = self.base_url + 'member/get_pending_relation_requests/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token, source=self.source,
                                          request_data=request_data, client_key_details_id=1, request_type="POST")
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_social.views.get_pending_relation_requests.utils.get_pending_relation_requests_response import \
                get_pending_relation_requests_response
            return get_pending_relation_requests_response(request_object=request_data, user=self.user,
                                                          access_token=self.access_token, source=self.source)
        else:
            pass
