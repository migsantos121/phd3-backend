from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel

from ib_notifications.constants.notification_choices import NOTIFICATION_CHOICES
from ib_notifications.models.notification_choices import NotificationChoice

__author__ = 'tanmay.ibhubs'


class UserNotificationChoice(AbstractDateTimeModel):
    user_id = models.IntegerField()
    notification_choice_id = models.IntegerField()
    preference = models.CharField(max_length=10, choices=NOTIFICATION_CHOICES, default='ON')

    def __unicode__(self):
        return unicode(str(self.user_id) + "/" + str(self.preference))

    class Meta:
        app_label = 'ib_notifications'

    def get_dictionary(self):
        dict = {
            'user_id': self.user_id,
            'notification_choice_id': self.notification_choice_id,
            'preference': self.preference,
            'id': self.id
        }
        return dict

    def get_minimal_dictionary(self):
        dict = {
            'notification_choice_id': self.notification_choice_id,
            'preference': self.preference,
            'id': self.id

        }
        return dict

    @classmethod
    def update_user_notification_preference(cls, user, source, name, preference):
        notification_choice = NotificationChoice.get_notification_choice(source, name)
        user_notification_choice, is_created = cls.objects.get_or_create(user_id=user.id,
                                                                         notification_choice_id=notification_choice.id)
        user_notification_choice.preference = preference
        user_notification_choice.save()
        from django.http import HttpResponse
        return HttpResponse()

    @classmethod
    def get_user_notification_choices(cls, source=None, name=None, preference=None):
        notification_choices = NotificationChoice.get_notification_choice(source, name)
        notification_choice_ids = notification_choices.keys()
        if preference is None:
            choice_list = cls.objects.filter(notification_choice_id__in=notification_choice_ids)
        else:
            choice_list = cls.objects.filter(notification_choice_id__in=notification_choice_ids, preference=preference)

        user_notification_dict_list = [obj.get_dictionary() for obj in choice_list]
        return user_notification_dict_list

    @classmethod
    def get_user_notification_choices_source(cls, source, user):
        notification_choices_objects = NotificationChoice.get_notification_choices_objects(source)
        notification_choice_ids = [each_notification_choice_object.id for each_notification_choice_object in
                                   notification_choices_objects]
        choice_list = list(cls.objects.filter(notification_choice_id__in=notification_choice_ids, user_id=user.id))
        user_notification_dict_list = UserNotificationChoice.get_unc_dictionary_list(notification_choices_objects,
                                                                                     choice_list)
        return user_notification_dict_list

    @staticmethod
    def get_unc_dictionary_list(notification_choices_objects, choice_list):
        dict_list = []
        for each_choice in choice_list:
            for each_notification_choice_object in notification_choices_objects:
                if each_choice.notification_choice_id == each_notification_choice_object.id:
                    dict_obj = dict()
                    dict_obj['name'] = each_notification_choice_object.name
                    dict_obj["source"] = each_notification_choice_object.source
                    dict_obj["display_name"] = each_notification_choice_object.display_name
                    dict_obj["preference"] = each_choice.preference
                    dict_list.append(dict_obj)
        return dict_list

    @classmethod
    def get_users_id_list(cls, notification_choice_id=None, preference='ON'):
        choice_list = cls.objects.filter(notification_choice_id=notification_choice_id, preference=preference)
        user_id_list = [obj.user_id for obj in choice_list]
        return user_id_list
