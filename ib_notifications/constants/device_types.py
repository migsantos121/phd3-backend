from enum import Enum


class DeviceType(Enum):
    DEFAULT = 'DEFAULT'
    ANDROID = 'ANDROID'
    IOS = 'IOS'
    WEB = 'WEB'
    WINDOWS = 'WINDOWS'


DEVICE_TYPES = [e.value for e in DeviceType]

