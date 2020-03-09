from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel


class IBUserRegistrationSource(AbstractDateTimeModel):
    ib_user = models.ForeignKey('ib_users.IBUser')
    registration_source = models.ForeignKey('ib_users.RegistrationSource')

    class Meta:
        app_label = 'ib_users'

    def __unicode__(self):
        return str(self.id)

    @staticmethod
    def create_user_registration_source(ib_user, registration_source):
        try:
            IBUserRegistrationSource.objects.get(ib_user=ib_user, registration_source=registration_source)
        except IBUserRegistrationSource.DoesNotExist:
            IBUserRegistrationSource.objects.create(ib_user=ib_user, registration_source=registration_source)
        return
