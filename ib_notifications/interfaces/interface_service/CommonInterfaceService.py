import os

from ib_notifications.constants.push_notification_types import PushNotificationTypes


class CommonInterface(object):
    def __init__(self, user, access_token, request_type):
        self.user = user
        self.access_token = access_token
        self.request_type = request_type
        self.branch = os.environ.get('DJANGO_SETTINGS_MODULE').split('.')[2]
        self.base_url = self.get_url()

    def get_url(self):
        if self.branch == 'local' or self.request_type == 'LIBRARY':
            base_url = 'http://127.0.0.1:8001/'
        else:
            base_url = os.environ.get('IB_NOTIFICATIONS_BASE_URL', '')
        return base_url + 'api/ib_notifications/'

    def send_notification_interface(self, source, name, title, message, extra_data, user_ids, cm_type,
                                    notification_type, log_notification, device_types=None,
                                    push_notification_type=PushNotificationTypes.DATA.value):
        if not device_types:
            device_types = []
        request_data = {
            'source': source,
            'name': name,
            'user_ids': user_ids,
            'cm_type': cm_type,
            'title': title,
            'message': message,
            'extra_data': extra_data,
            'log_notification': log_notification,
            'notification_type': notification_type,
            'device_types': device_types,
            'push_notification_type': push_notification_type,
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'notifications/send_notification/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def get_notifications(self, source, offset, limit):
        request_data = dict([
            ('source', source),
            ('offset', offset),
            ('limit', limit)
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'notifications/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def read_notification(self, notification_id, user_ids):
        request_data = dict([
            ('user_ids', user_ids),
            ('notification_id', notification_id)
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'notifications/read/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def add_notification_choice(self, source, name, display_name, default):
        request_data = {
            'source': source,
            'name': name,
            'display_name': display_name,
            'default': default
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'notifications/add_notification_choice/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def update_user_notification_choice(self, name, source, preference):
        request_data = {
            'name': name,
            'preference': preference,
            'source': source
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'notifications/update_user_notification_choice/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def add_user_token(self, source, cm_type, cm_token):
        request_data = {
            'source': source,
            'cm_type': cm_type,
            'cm_token': cm_token
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'notifications/add_user_token/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def get_user_notification_choices(self, source):
        request_data = {
            'source': source
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'notifications/get_user_notification_choices/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def send_real_time_data(self, real_time_event_data_list):
        if self.request_type == 'SERVICE':
            url = self.base_url + 'send_real_time_data_api/v1/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=real_time_event_data_list, client_key_details_id=1)
            return response_object
        else:
            pass

    def deactivate_user_cm_tokens(self, source, user_id, device_types, device_id='', cm_token=''):
        if self.request_type == 'SERVICE':
            url = self.base_url + 'notifications/deactivate/'
            request_data = {'source': source, 'user_id': user_id, 'device_types': device_types,
                            'device_id': device_id, 'cm_token': cm_token}
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def add_member_to_notification_group(self, user_ids, entity_id, entity_type, group_name, group_type, source):
        request_data = {
            "user_ids": user_ids,
            "entity_id": entity_id,
            "entity_type": entity_type,
            "group_name": group_name,
            "group_type": group_type,
            "source": source
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'notifications/add_member_to_group/'

            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def get_groups(self, offset, filters, source, group_type):
        request_data = {
            "offset": offset,
            "filter": filters,
            "source": source,
            "group_type": group_type
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'notifications/groups/'

            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def send_group_notifications(self, source, name, entity_id, entity_type, cm_type, title, message, extra_data,
                                 log_notification, notification_type):
        request_data = {
            "source": source,
            "name": name,
            "entity_id": entity_id,
            "entity_type": entity_type,
            "cm_type": cm_type,
            "title": title,
            "message": message,
            "extra_data": extra_data,
            "log_notification": log_notification,
            "notification_type": notification_type
        }

        if self.request_type == 'SERVICE':
            url = self.base_url + 'notifications/groups/'

            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass