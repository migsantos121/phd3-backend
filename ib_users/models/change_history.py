from django.db import models

from ib_users.constants.type import FIELD_UPDATE_TYPE

__author__ = 'tanmay.ibhubs'

from ib_common.models.abstract_date_time_model import AbstractDateTimeModel


class ChangeHistoryManager(models.Manager):
    def get_queryset(self):
        return super(ChangeHistoryManager, self).get_queryset().filter(
            is_deleted=False)


class ChangeHistory(AbstractDateTimeModel):
    user_id = models.IntegerField(null=False)
    old_val = models.CharField(max_length=100, default='')
    new_val = models.CharField(max_length=100, default='')
    is_verified = models.BooleanField(default=False)
    type = models.CharField(max_length=100, choices=FIELD_UPDATE_TYPE,
                            default='NONE')
    is_deleted = models.BooleanField(default=False)
    objects = ChangeHistoryManager()

    def __unicode__(self):
        return str("%s-%s" % (self.user_id, self.id))

    class Meta:
        app_label = 'ib_users'

    @classmethod
    def create_change_history(cls, user_id, old_val, new_val, is_verified,
                              type):
        if old_val is None:
            old_val = ''

        change_history = cls.objects.create(
            user_id=user_id,
            old_val=old_val,
            new_val=new_val,
            is_verified=is_verified,
            type=type
        )
        return change_history
