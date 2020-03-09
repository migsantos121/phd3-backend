from abc import ABCMeta, abstractmethod

__author__ = 'tanmay.ibhubs'


class AbstractCMHandler(object):
    __metaclass__ = ABCMeta

    @staticmethod
    def clean_push_notification_type(push_notification_type=None):
        if push_notification_type is None or not push_notification_type:
            from ib_notifications.constants.push_notification_types import PushNotificationTypes
            push_notification_type = PushNotificationTypes.DATA.value
        return push_notification_type

    @abstractmethod
    def register_topic(self, channel_id, user_fcm_tokens):
        pass

    @abstractmethod
    def unregister_topic(self, channel_id, user_fcm_tokens):
        pass

    @abstractmethod
    def send_data_to_topic(self, channel_id, title, message, extra_data):
        pass

    @abstractmethod
    def send_data_to_multiple_user(self, receivers_token_list, title, message, extra_data, notification_type,
                                   push_notification_type):
        pass
