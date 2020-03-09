from enum import Enum

__author__ = 'tanmay.ibhubs'

USER = 'USER'
FRIEND = 'FRIEND'
FOLLOWER = 'FOLLOW'
FB_FRIEND = 'FB_FRIEND'


class Variables(Enum):
    USER = 'USER'


class RelationshipStatus(Enum):
    ACCEPT = "ACCEPT"
    PENDING = "PENDING"
    REJECT = "REJECT"


class Relations(Enum):
    FRIEND = 'FRIEND'
    FOLLOWER = 'FOLLOW'
    FB_FRIEND = 'FB_FRIEND'

