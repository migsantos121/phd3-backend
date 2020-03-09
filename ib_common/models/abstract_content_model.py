from django.db import models
from ib_common.models.abstract_multimedia_model import AbstractMultimediaModel
from ib_common.constants.content_type import ContentTypesEnum

__author__ = 'kapeed2091'


class AbstractContentModel(AbstractMultimediaModel):
    _content = models.TextField(blank=True, default='', null=True)
    _content_type = models.CharField(max_length=100, default=ContentTypesEnum.TEXT.value)

    class Meta:
        abstract = True

    @property
    def content(self):
        return self._i_content

    @property
    def content_type(self):
        return self._i_content_type
