from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel


class KeywordGroup(AbstractDateTimeModel):
    group = models.CharField(max_length=500)
    sub_group = models.CharField(max_length=500, blank=True, null=True)
    group_weight = models.FloatField()

    def __unicode__(self):
        return unicode(self.group)
