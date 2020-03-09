from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel


class RegistrationSource(AbstractDateTimeModel):
    registration_source = models.CharField(max_length=100)

    class Meta:
        app_label = 'ib_users'

    def __unicode__(self):
        return self.registration_source
