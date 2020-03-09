import os

from ib_notifications.constants.push_notification_types import PushNotificationTypes


class CommonInterface(object):
    def __init__(self, user, access_token, request_type):
        self.user = user
        self.access_token = access_token
        self.request_type = request_type
        self.branch = os.environ.get('DJANGO_SETTINGS_MODULE').split('.')[2]
        self.interface_service = self.make_interface_service_call()

    def make_interface_service_call(self):
        from ib_notifications.interfaces.interface_service.CommonInterfaceService import CommonInterface as Service
        interface_service = Service(self.user, self.access_token, self.request_type)
        return interface_service

    def send_notification_interface(self, source, name, title, message, extra_data, user_ids, cm_type,
                                    notification_type, log_notification, device_types=None,
                                    push_notification_type=PushNotificationTypes.DATA.value):
        if not device_types:
            device_types = []

        if self.request_type == 'SERVICE':
            response_object = self.interface_service.send_notification_interface(name=name,
                                                                                 title=title,
                                                                                 source=source,
                                                                                 cm_type=cm_type,
                                                                                 message=message,
                                                                                 user_ids=user_ids,
                                                                                 extra_data=extra_data,
                                                                                 log_notification=log_notification,
                                                                                 device_types=device_types,
                                                                                 push_notification_type=
                                                                                 push_notification_type,
                                                                                 notification_type=notification_type)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_notifications.models.user_cm_tokens import UserCMToken
            response_object = UserCMToken.send_notification(name=name,
                                                            title=title,
                                                            source=source,
                                                            user=self.user,
                                                            cm_type=cm_type,
                                                            message=message,
                                                            extra_data=extra_data,
                                                            user_id_list=user_ids,
                                                            log_notification=log_notification,
                                                            notification_type=notification_type,
                                                            device_types=device_types,
                                                            push_notification_type=
                                                            push_notification_type,
                                                            )
            return response_object
        else:
            pass

    def get_notifications(self, source, offset, limit):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.get_notifications(source, offset, limit)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_notifications.models.notification import Notification
            response_object = Notification.get_notifications_objects(source=source, offset=offset, limit=limit,
                                                                     user=self.user, access_token=self.access_token)
            return response_object
        else:
            pass

    def read_notification(self, notification_id, user_ids):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.read_notification(notification_id, user_ids)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_notifications.models import Notification
            response_object = Notification.update_notification_read_status(notification_id, user_ids)
            return response_object
        else:
            pass

    def add_notification_choice(self, source, name, display_name, default):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.add_notification_choice(source, name, display_name, default)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_notifications.models.notification_choices import NotificationChoice
            response_object = NotificationChoice.add_notification_choice(source=source, name=name,
                                                                         display_name=display_name, default=default)
            return response_object
        else:
            pass

    def update_user_notification_choice(self, name, source, preference):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.update_user_notification_choice(name, source, preference)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_notifications.models.user_notification_choices import UserNotificationChoice
            response_object = UserNotificationChoice.update_user_notification_preference(
                source=source, name=name, preference=preference, user=self.user)
            return response_object
        else:
            pass

    def get_user_notications_choices_interface(self, source):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.get_user_notications_choices_interface(source)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_notifications.models.user_notification_choices import UserNotificationChoice
            response_object = UserNotificationChoice.get_user_notification_choices_source(source=source,
                                                                                          user=self.user)
            return response_object
        else:
            pass

    def add_user_token_interface(self, source, cm_type, cm_token):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.add_user_token(source, cm_type, cm_token)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_notifications.models.user_cm_tokens import UserCMToken
            response_object = UserCMToken.update_user_cm_tokens(source=source, user=self.user, cm_type=cm_type,
                                                                cm_token=cm_token)
            return response_object
        else:
            pass

    def get_user_notification_choices(self, source):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.get_user_notification_choices(source)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_notifications.models.user_notification_choices import UserNotificationChoice
            response_object = UserNotificationChoice.get_user_notification_choices_source(source=source, user=self.user)
            return response_object
        else:
            pass

    def send_real_time_data(self, real_time_event_data_list):  # [{'real_time_event': '', 'real_time_data': ''}]
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.send_real_time_data(real_time_event_data_list)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_notifications.api_wrappers.send_real_time_data import send_real_time_data
            response_object = send_real_time_data(real_time_event_data_list)
            return response_object

    def deactivate_user_cm_tokens(self, source, user_id, device_types, device_id='', cm_token=''):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.deactivate_user_cm_tokens(source, user_id, device_types)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_notifications.views.deactivate_user_cm_tokens_api.api_wrapper import api_wrapper
            response_object = api_wrapper(request_data={'source': source,
                                                        'user_id': user_id,
                                                        'device_types': device_types,
                                                        'device_id': device_id,
                                                        'cm_token': cm_token},
                                          source='',
                                          user=self.user,
                                          access_token=self.access_token)
            return response_object

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
            response_object = self.interface_service.add_member_to_notification_group(user_ids, entity_id, entity_type,
                                                                                      group_name, group_type, source)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_notifications.views.add_member_to_group.api_wrapper import api_wrapper
            response_object = api_wrapper(request_data=request_data, user=self.user, access_token=self.access_token, source='')
            return response_object

    def get_groups(self, offset, filters, source, group_type):
        request_data = {
            "offset": offset,
            "filter": filters,
            "source": source,
            "group_type": group_type
        }
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.get_groups(offset, filters, source, group_type)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_notifications.views.get_groups.api_wrapper import api_wrapper
            response_object = api_wrapper(request_data=request_data, user=self.user, access_token=self.access_token, source=source)
            return response_object

    def send_group_notifications(self, source, name, entity_id, entity_type, cm_type, title, message, extra_data,
                                 log_notification, notification_type, push_notification_type=PushNotificationTypes.DATA.value):
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
            "notification_type": notification_type,
            "push_notification_type":push_notification_type
        }
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.send_group_notifications(source, name, entity_id, entity_type, cm_type, title, message, extra_data,
                                 log_notification, notification_type)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_notifications.views.send_notification_to_group.api_wrapper import api_wrapper
            response_object = api_wrapper(request_data=request_data, user=self.user, access_token=self.access_token, source=source)
            return response_object
