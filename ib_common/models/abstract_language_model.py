from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel


class AbstractLanguageModel(AbstractDateTimeModel):
    #TODO: Add custom validators for field
    from ib_common.constants.language_choices import DEFAULT_LANGUAGE
    language_name = models.CharField(max_length=100, default=DEFAULT_LANGUAGE)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        from ib_common.constants.language_choices import LANGUAGES
        if self.language_name not in LANGUAGES:
            raise Exception('Invalid Language')
        super(AbstractLanguageModel, self).save(*args, **kwargs)
