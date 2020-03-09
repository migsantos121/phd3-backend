from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel

from ib_notifications.models.notification_receiver import NotificationReceiver


class Notification(AbstractDateTimeModel):
    message = models.CharField(max_length=1000, null=True, blank=True)
    extra_data = models.TextField(max_length=1000000000, null=True, blank=True)
    title = models.CharField(max_length=500, default="iBHubs")
    source = models.CharField(max_length=255)
    created_by = models.IntegerField()
    cm_type = models.CharField(max_length=255)
    members = models.ManyToManyField(NotificationReceiver)
    notification_type = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return unicode("%s" % self.title)

    class Meta:
        app_label = 'ib_notifications'

    @staticmethod
    def get_notifications_objects(source, offset, limit, user, access_token, sort_by_date=None):
        notifications = Notification.objects.prefetch_related('members').filter(source=source, members__user_id=user.id)

        if sort_by_date:
            if sort_by_date == 'ASC':
                notifications = notifications.order_by('creation_datetime')
            else:
                notifications = notifications.order_by('-creation_datetime')
        total = notifications.count()
        if limit > 0:
            notifications = notifications[offset:offset + limit]
        notification_response_objects = []

        user_ids = [notification.created_by for notification in notifications]
        from ib_notifications.adapters.get_names_from_userids_adapter import get_names_from_userids_adapter
        user_name_objects = get_names_from_userids_adapter(user=user, access_token=access_token, user_ids=user_ids)

        user_name_dict = {user_object["user_id"]: user_object.get("name", "") for user_object in user_name_objects}

        for each_notification in notifications:
            user_name = user_name_dict.get(each_notification.created_by)
            notification_response_object = Notification.get_notification_object(each_notification, user_name)
            notification_response_objects.append(notification_response_object)
        response_object = {
            "total": total,
            "notifications": notification_response_objects
        }
        return response_object

    @classmethod
    def get_user_notifications_object(cls, source, offset, limit, user, sort_by_date=None):
        notifications = cls.objects.prefetch_related('members').filter(source=source, members__user_id=user.id).distinct()

        if sort_by_date:
            if sort_by_date == 'ASC':
                notifications = notifications.order_by('creation_datetime')
            else:
                notifications = notifications.order_by('-creation_datetime')
        total_count = notifications.count()
        unread_count = notifications.filter(members__user_id=user.id, members__read_status=False).count()

        if limit > 0:
            notifications = notifications[offset:offset + limit]
        notification_response_objects = []

        for each_notification in notifications:
            notification_response_object = Notification.get_user_notification_object(each_notification, user.id)
            notification_response_objects.append(notification_response_object)
        response_object = {
            "total_count": total_count,
            "unread_count": unread_count,
            "notifications": notification_response_objects
        }
        return response_object

    @staticmethod
    def get_user_notification_object(notification, user_id):
        return {
            'title': notification.title,
            'message': notification.message,
            'notification_id': notification.id,
            'extra_data': notification.extra_data,
            'notification_type': notification.notification_type,
            'creation_datetime': notification.creation_datetime,
            'read_at': notification.members.filter(user_id=user_id)[0].read_at,
            'read_status': notification.members.filter(user_id=user_id)[0].read_status
        }

    @staticmethod
    def get_notification_object(notification, created_by_name):
        notification_response_object = dict()
        notification_response_object["title"] = notification.title
        notification_response_object["cm_type"] = notification.cm_type
        notification_response_object["message"] = notification.message
        notification_response_object["notification_id"] = notification.id
        notification_response_object["extra_data"] = notification.extra_data
        notification_response_object["notification_type"] = notification.notification_type
        if created_by_name:
            notification_response_object["created_by"] = created_by_name
        member_objects = Notification.get_member_objects(notification)
        notification_response_object["members_details"] = member_objects
        notification_response_object['creation_datetime'] = notification.creation_datetime
        return notification_response_object

    @staticmethod
    def get_member_objects(notification):
        member_objects = list()
        members = notification.members.values('user_id', 'read_status', 'cm_token', 'read_at')
        for each_member in members:
            member_object = NotificationReceiver.get_member_object(each_member)
            member_objects.append(member_object)
        return member_objects

    @staticmethod
    def save_and_get_notification_details(source, cm_type, title, message, extra_data, user_cm_tokens_objects, user,
                                          notification_type):
        notification = Notification.objects.create(cm_type=cm_type, source=source, title=title,
                                                   created_by=user.id, extra_data=str(extra_data),
                                                   notification_type=notification_type, message=message)
        receivers_objects_list = NotificationReceiver.save_and_get_notification_receivers_list(user_cm_tokens_objects)
        notification.members.add(*receivers_objects_list)
        notification.save()
        return notification

    @staticmethod
    def update_notification_read_status(notification_id, user_ids):
        notification_object = Notification.objects.get(pk=notification_id)
        notification_receivers = notification_object.members.filter(user_id__in=user_ids)
        NotificationReceiver.update_notification_receiver(notification_receivers)
        from django.http import HttpResponse
        return HttpResponse()
