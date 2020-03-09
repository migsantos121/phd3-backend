from enum import Enum

__author__ = 'vedavidh'


class ServiceTypesEnum(Enum):
    SERVICE = 'SERVICE'
    LIBRARY = 'LIBRARY'

SERVICE_TYPE_CHOICES = [(e.value, e.value) for e in ServiceTypesEnum]

SERVICE_TYPES = [e.value for e in ServiceTypesEnum]
