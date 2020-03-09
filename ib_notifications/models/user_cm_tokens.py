from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel

from ib_notifications.constants.cloud_type import CLOUD_TYPE
from ib_notifications.constants.device_types import DeviceType
from ib_notifications.constants.push_notification_types import PushNotificationTypes
from ib_notifications.constants.user_cm_token_status_types import UserCMTokenStatusTypes
from ib_notifications.controllers.cm_service_controller import CMServiceAPI
from ib_notifications.models.notification_choices import NotificationChoice
from ib_notifications.models.user_notification_choices import UserNotificationChoice

__author__ = 'tanmay.ibhubs'


class UserCMToken(AbstractDateTimeModel):
    user_id = models.IntegerField()
    cm_type = models.CharField(max_length=10, choices=CLOUD_TYPE)
    cm_token = models.CharField(max_length=300)
    source = models.CharField(max_length=300)
    device_id = models.TextField()
    device_type = models.TextField(default=DeviceType.ANDROID.value)
    status = models.CharField(max_length=200, default=UserCMTokenStatusTypes.ACTIVE.value)

    def __unicode__(self):
        return unicode(str(self.user_id) + "/" + str(self.cm_type))

    class Meta:
        app_label = 'ib_notifications'

    def get_dictionary(self):
        dict = {
            'user_id': self.user_id,
            'cm_type': self.cm_type,
            'cm_token': self.cm_token,
            'source': self.source
        }
        return dict

    @classmethod
    def update_user_cm_tokens(cls, user, cm_type, cm_token, source, device_id='', device_type=DeviceType.DEFAULT.value):

        from django.db.models import Q

        cls.objects.filter(Q(user_id=user.id, cm_type=cm_type, device_id=device_id, device_type=device_type,
                             source=source) | Q(cm_token=cm_token, source=source)) \
            .update(status=UserCMTokenStatusTypes.DEACTIVATED.value)

        cls.objects.create(user_id=user.id, cm_type=cm_type, source=source,
                           cm_token=cm_token, device_id=device_id, device_type=device_type)
        from django.http import HttpResponse
        return HttpResponse()

    @classmethod
    def get_users_cm_token(cls, user_id_list=None, cm_type=None, source=None):
        user_token_query_list = cls.objects.filter(user_id__in=user_id_list, cm_type=cm_type, source=source)
        user_token_dict_list = [user_token.get_dictionary() for user_token in user_token_query_list]
        return user_token_dict_list

    @classmethod
    def send_notification(cls, source, name, title, message, extra_data, user_id_list, cm_type, log_notification, user,
                          notification_type, device_types=None,
                          push_notification_type=PushNotificationTypes.DATA.value):
        if user.id in user_id_list:
            user_id_list.remove(user.id)

        import json
        if extra_data:
            extra_data_dict = json.loads(extra_data)
        else:
            extra_data_dict = {}

        notification_choice, is_created = NotificationChoice.objects.get_or_create(source=source, name=name)
        if notification_choice.default_choice == "ON":
            unsubscribed_user_list = UserNotificationChoice.get_users_id_list(
                notification_choice_id=notification_choice.id, preference='OFF')
            receivers_list = list(set(user_id_list) - set(unsubscribed_user_list))
        else:
            receivers_list = UserNotificationChoice.get_users_id_list(notification_choice_id=notification_choice.id)

        query_set = cls.objects.filter(user_id__in=receivers_list, cm_type=cm_type, source=source,
                                       status=UserCMTokenStatusTypes.ACTIVE.value)
        if device_types:
            query_set = query_set.filter(device_type__in=device_types)

        user_cm_tokens_objects = query_set.values('user_id', 'cm_token')
        receiver_tokens = [each_cm_token_object["cm_token"] for each_cm_token_object in user_cm_tokens_objects]
        user_ids = [each_cm_token_object["user_id"] for each_cm_token_object in user_cm_tokens_objects]

        if log_notification:
            from ib_notifications.models import Notification
            notification = Notification.save_and_get_notification_details(title=title, message=message,
                                                                          source=source, cm_type=cm_type,
                                                                          extra_data=extra_data, user=user,
                                                                          notification_type=notification_type,
                                                                          user_cm_tokens_objects=user_cm_tokens_objects)
            notification_id = notification.id
        else:
            notification_id = -1
        extra_data_dict['notification_id'] = notification_id
        extra_data = json.dumps(extra_data_dict)
        from ib_notifications.constants.cm_type import CloudMessagingType
        if cm_type == CloudMessagingType.SOCKET.name:
            from ib_notifications.views.send_notification.utils.send_through_socket import send_data_through_socket
            send_data_through_socket(title=title, message=message, extra_data=extra_data, user_ids=user_ids)
        else:
            cm_service = CMServiceAPI(cm_type=cm_type)
            cm_service.send_data_to_multiple_user(message=message, title=title,
                                                  extra_data=extra_data,
                                                  notification_type=notification_type,
                                                  receivers_token_list=list(receiver_tokens),
                                                  push_notification_type=push_notification_type)

        return {"notification_id": notification_id}

    @classmethod
    def deactivate_tokens(cls, source, user_id='', cm_token='', device_id='', device_types=None):

        if cm_token:
            cls.objects.filter(cm_token=cm_token, source=source) \
                .update(status=UserCMTokenStatusTypes.DEACTIVATED.value)
        elif device_id and user_id:
            cls.objects.filter(user_id=user_id, device_id=device_id, source=source) \
                .update(status=UserCMTokenStatusTypes.DEACTIVATED.value)
        else:
            cls.objects.filter(user_id=user_id, source=source, device_type__in=device_types) \
                .update(status=UserCMTokenStatusTypes.DEACTIVATED.value)
        return
