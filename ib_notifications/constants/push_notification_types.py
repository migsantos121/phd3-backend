from enum import Enum


class PushNotificationTypes(Enum):
    """
    PushNotificationTypes constant is used to distinguish notification and data type notifications in fcm
    """
    NOTIFICATION = 'NOTIFICATION'
    DATA = 'DATA'
