from django.db import models
from ib_common.models.abstract_language_model import AbstractLanguageModel


class AbstractVernacularContentModel(AbstractLanguageModel):
    from ib_common.constants.multimedia_type import MULTIMEDIA_TYPE
    from ib_common.utilities.multimedia_file_name import multimedia_file_name
    from ib_common.utilities.multimedia_thumbnail_file_name import multimedia_thumbnail_file_name
    v_content = models.CharField(max_length=1000)
    v_content_type = models.CharField(max_length=100, default='text')
    v_multimedia_type = models.CharField(max_length=1000, null=True, blank=True, default='text',
                                         choices=MULTIMEDIA_TYPE)
    v_multimedia = models.FileField(upload_to=multimedia_file_name, null=True, blank=True, max_length=1000)
    v_multimedia_thumbnail = models.FileField(upload_to=multimedia_thumbnail_file_name, null=True, blank=True,
                                              max_length=1000)

    class Meta:
        abstract = True
