from django.conf import settings
from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed

from ib_notifications.constants.cm_type import CloudMessagingType
from ib_notifications.utilities.abstract_cm_handler import AbstractCMHandler
from ib_notifications.constants.push_notification_types import PushNotificationTypes

__author__ = 'tanmay.ibhubs'


class CMServiceAPI(AbstractCMHandler):
    def __init__(self, *args, **kwargs):
        cm_type = kwargs["cm_type"]
        if cm_type == CloudMessagingType.FCM.value:
            from ib_notifications.controllers.fcm_controller import FirebaseController
            self.handler = FirebaseController(*args, **kwargs)
        elif cm_type == CloudMessagingType.ONE_SIGNAL.value:
            from ib_notifications.controllers.onesignal_controller import OneSignalController
            self.handler = OneSignalController(*args, **kwargs)
        elif cm_type == CloudMessagingType.PUB_NUB.value:
            raise ExpectationFailed({}, res_status="PUB_NUB not implemented")
        else:
            raise ExpectationFailed({}, res_status="CM_TYPE not available to use")

    def register_topic(self, channel_id, user_fcm_tokens):
        return self.handler.register_topic(channel_id=channel_id, user_fcm_tokens=user_fcm_tokens)

    def unregister_topic(self, channel_id, user_fcm_tokens):
        return self.handler.unregister_topic(channel_id=channel_id, user_fcm_tokens=user_fcm_tokens)

    def send_data_to_topic(self, channel_id, title, message, extra_data):
        return self.handler.send_data_to_topic(channel_id=channel_id, title=title, message=message,
                                               extra_data=extra_data)

    def send_data_to_multiple_user(self, receivers_token_list, title, message, extra_data, notification_type,
                                   push_notification_type=PushNotificationTypes.DATA.value):
        return self.handler.send_data_to_multiple_user(receivers_token_list=receivers_token_list,
                                                       title=title, message=message, extra_data=extra_data,
                                                       notification_type=notification_type,
                                                       push_notification_type=push_notification_type)
