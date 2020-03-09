from enum import Enum

__author__ = 'kapeed2091'


class MultimediaTypesEnum(Enum):
    TEXT = 'text'
    IMAGE = 'image'
    AUDIO = 'audio'
    VIDEO = 'video'


MULTIMEDIA_TYPE = [(e.value, e.value) for e in MultimediaTypesEnum]

MULTIMEDIA_TYPES_LIST = [e.value for e in MultimediaTypesEnum]
