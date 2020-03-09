from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel
from ib_common.vernacular_utils.vernacular_utilities_class import VernacularUtilitiesClass

__author__ = 'kapeed2091'


class AbstractMultimediaModel(AbstractDateTimeModel, VernacularUtilitiesClass):
    from ib_common.constants.multimedia_type import MULTIMEDIA_TYPE
    from ib_common.utilities.multimedia_file_name import multimedia_file_name
    from ib_common.utilities.multimedia_thumbnail_file_name import multimedia_thumbnail_file_name
    _multimedia_type = models.CharField(max_length=1000, null=True, blank=True, default='text', choices=MULTIMEDIA_TYPE)
    _multimedia = models.FileField(upload_to=multimedia_file_name, null=True, blank=True, max_length=1000)
    _multimedia_thumbnail = models.FileField(upload_to=multimedia_thumbnail_file_name, null=True, blank=True,
                                             max_length=1000)

    class Meta:
        abstract = True

    @property
    def multimedia_type(self):
        return self._i_multimedia_type

    @property
    def multimedia(self):
        from ib_common.utilities.get_absolute_file_path_for_multimedia import get_absolute_file_path_for_multimedia
        return get_absolute_file_path_for_multimedia(self._i_multimedia)

    @property
    def multimedia_thumbnail(self):
        from ib_common.utilities.get_absolute_file_path_for_multimedia import get_absolute_file_path_for_multimedia
        return get_absolute_file_path_for_multimedia(self._i_multimedia_thumbnail)
