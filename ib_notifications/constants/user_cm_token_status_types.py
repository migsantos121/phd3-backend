from enum import Enum


class UserCMTokenStatusTypes(Enum):
    ACTIVE = 'ACTIVE'
    DEACTIVATED = 'DEACTIVATED'


USER_CM_TOKEN_STATUS_TYPES_LIST = [e.value for e in UserCMTokenStatusTypes]

