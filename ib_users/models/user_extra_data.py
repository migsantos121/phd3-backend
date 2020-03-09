__author__ = 'tanmay.ibhubs'

from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel


class UserExtraData(AbstractDateTimeModel):
    ib_user = models.ForeignKey('ib_users.IBUser', related_name='user_extra_data')
    source = models.CharField(max_length=25, default='', null=False)
    ud_key = models.CharField(max_length=25, default='', null=False)
    ud_value = models.CharField(max_length=500)

    class Meta:
        verbose_name = "User Extra Data"
        unique_together = (('ib_user', 'source', 'ud_key'),)
        app_label = 'ib_users'

    def __unicode__(self):
        return str(self.ib_user) + "/" + str(self.source)

    def convert_to_ud_dict(self):
        return {
            'ud_key': self.ud_key,
            'ud_value': self.ud_value
        }

    @classmethod
    def add_key_value_pair(cls, user, key, value, source):
        try:
            extra_data = cls.objects.get(ib_user=user, source=source,
                                         ud_key=key)
            extra_data.ud_value = value
            extra_data.save()
        except cls.DoesNotExist:
            cls.objects.create(ib_user=user, source=source, ud_key=key,
                               ud_value=value)

        return

    @classmethod
    def get_extra_data_for_user(cls, user, source):
        response_list = cls.objects.filter(ib_user=user, source=source).values('ud_key', 'ud_value')
        return response_list
