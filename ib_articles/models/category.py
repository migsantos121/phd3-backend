from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel


class Category(AbstractDateTimeModel):
    name = models.URLField(max_length=255, unique=True)

    def __unicode__(self):
        return unicode(self.name)