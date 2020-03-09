from enum import Enum

__author__ = 'tanmay.ibhubs'

CLOUD_TYPE = (
    (u'FCM', u'FCM'),
    (u'ONESIGNAL', u'ONESIGNAL'),
    (u'PUBNUB', u'PUBNUB'),
    (u'SOCKET', u'SOCKET'),
)

GROUP_TYPE = (
    (u'GENERAL', u'GENERAL'),
)


class GroupType(Enum):
    GENERAL = 'GENERAL'
