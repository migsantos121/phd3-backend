from datetime import datetime
from django.db import models

from ib_common.models.abstract_date_time_model import AbstractDateTimeModel


class NotificationReceiver(AbstractDateTimeModel):
    user_id = models.CharField(max_length=100)
    read_status = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    cm_token = models.TextField(max_length=10000, null=True, blank=True)
    created_time = models.DateTimeField()

    def __unicode__(self):
        return unicode("%s" % self.id)

    class Meta:
        app_label = 'ib_notifications'

    @classmethod
    def save_and_get_notification_receivers_list(cls, user_cm_tokens_objects):
        notification_receiver_objects = list()
        created_time = datetime.now()
        for each_user_cm_token_object in user_cm_tokens_objects:
            notification_receiver = NotificationReceiver(created_time=created_time,
                                                         user_id=each_user_cm_token_object["user_id"],
                                                         cm_token=each_user_cm_token_object["cm_token"])
            notification_receiver_objects.append(notification_receiver)
        NotificationReceiver.objects.bulk_create(notification_receiver_objects)
        notification_receivers = NotificationReceiver.objects.filter(created_time=created_time)
        return notification_receivers

    @staticmethod
    def get_member_object(member):
        user_id = member["user_id"]
        read_status = member["read_status"]
        read_at = member["read_at"]
        device_ids_string = member["cm_token"]
        cm_token = device_ids_string.split(",")
        member_object = {
            "user_id": user_id,
            "read_status": read_status,
            "read_at": read_at,
            "cm_token": cm_token
        }
        return member_object

    @staticmethod
    def update_notification_receiver(notification_receivers):
        notification_receivers.update(read_status=True, read_at=datetime.now())
