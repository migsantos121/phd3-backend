from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel


class NewsSource(AbstractDateTimeModel):
    name = models.CharField(max_length=200, unique=True)
    url = models.URLField(max_length=500)

    def __unicode__(self):
        return unicode(self.name)
