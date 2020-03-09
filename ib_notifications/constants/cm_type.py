__author__ = 'tanmay.ibhubs'
from enum import Enum


class CloudMessagingType(Enum):
    FCM = 'FCM'
    ONE_SIGNAL = 'ONE_SIGNAL'
    PUB_NUB = "PUB_NUB"
    SOCKET = "SOCKET"
