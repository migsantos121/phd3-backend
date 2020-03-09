from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel

from ib_notifications.constants.notification_choices import NOTIFICATION_CHOICES

__author__ = 'tanmay.ibhubs'


class NotificationChoice(AbstractDateTimeModel):
    source = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=30)
    default_choice = models.CharField(max_length=10, choices=NOTIFICATION_CHOICES, default='ON')

    class Meta:
        unique_together = ('source', 'name')
        app_label = 'ib_notifications'

    def __unicode__(self):
        return unicode(self.display_name + "/" + self.default_choice)

    @classmethod
    def add_notification_choice(cls, source, name, display_name, default_choice):
        notification_choice, is_created = cls.objects.get_or_create(source=source, name=name)
        if is_created:
            notification_choice.default_choice = default_choice
            notification_choice.display_name = display_name
            notification_choice.save()
        from django.http import HttpResponse
        return HttpResponse()

    @classmethod
    def get_notification_choice(cls, source, name):
        try:
            notification_choice = cls.objects.get(source=source, name=name)
            return notification_choice
        except:
            from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed
            raise ExpectationFailed({}, "Notification choice object not exist")

    @classmethod
    def get_notification_choices_objects(cls, source):
        notification_choice_objects = list(cls.objects.filter(source=source))
        return notification_choice_objects
