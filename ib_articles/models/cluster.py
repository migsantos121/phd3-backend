from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel


class Cluster(AbstractDateTimeModel):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)
