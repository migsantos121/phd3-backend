from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel

from ib_users.constants.type import SOCIAL_PROVIDER_TYPE

__author__ = 'tanmay.ibhubs'


class SocialProvider(AbstractDateTimeModel):
    name = models.CharField(max_length=15, choices=SOCIAL_PROVIDER_TYPE, blank=True, null=True)

    class Meta:
        verbose_name = "Social Provider"
        app_label = 'ib_users'

    def __unicode__(self):
        return str(self.name)
