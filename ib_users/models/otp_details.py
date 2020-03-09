from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel


class OTPDetails(AbstractDateTimeModel):
    ib_user = models.OneToOneField('ib_users.IBUser', on_delete=models.CASCADE)
    otp_count = models.IntegerField()

    class Meta:
        app_label = 'ib_users'
