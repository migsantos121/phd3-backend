from enum import Enum

__author__ = 'kapeed2091'


class ContentTypesEnum(Enum):
    TEXT = 'text'
    LATEX = 'latex'

CONTENT_TYPE = [(e.value, e.value) for e in ContentTypesEnum]

CONTENT_TYPES_LIST = [e.value for e in ContentTypesEnum]
