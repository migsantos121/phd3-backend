from enum import Enum

__author__ = 'vedavidh'


class LanguageEnum(Enum):
    ENGLISH = 'ENGLISH'
    HINDI = 'HINDI'
    TELUGU = 'TELUGU'
    TAMIL = 'TAMIL'

LANGUAGE_CHOICES = [(e.value, e.value) for e in LanguageEnum]

LANGUAGES = [e.value for e in LanguageEnum]

DEFAULT_LANGUAGE = LanguageEnum.ENGLISH.value
