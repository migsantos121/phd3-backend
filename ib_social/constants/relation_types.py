__author__ = 'tanmay.ibhubs'

SYMMETRIC_RELATION_TYPES = [
    ('FRIEND', 'Friend'),
    ('FB_FRIEND', 'Facebook Friend'),
]

SYMMETRIC_RELATIONS = [item[0] for item in SYMMETRIC_RELATION_TYPES]


ASYMMETRIC_RELATION_TYPES = [
    ('FOLLOW', 'Following'),
    ('BLOCK', 'Block'),
]

RELATION_TYPES = SYMMETRIC_RELATION_TYPES + ASYMMETRIC_RELATION_TYPES

NEGATIVE_RELATIONS = ["UNFOLLOW", "UNFRIEND", "FB_UNFRIEND", "UNBLOCK"]

OPPOSITE_RELATION = {
    "UNFOLLOW": "FOLLOW",
    "FB_UNFRIEND": "FB_FRIEND",
    "UNFRIEND": "FRIEND",
    "UNBLOCK": "BLOCK",
    "BLOCK": ["FRIEND", "FB_FRIEND", "FOLLOW"]
}


RELATION_STATUSES = [
    ('ACCEPT', 'Accept'),
    ('PENDING', 'Pending'),
    ('WAITING_FOR_APPROVAL', 'Waiting for Approval'),
    ('REJECT', 'Reject'),
]
