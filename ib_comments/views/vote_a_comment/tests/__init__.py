# Endpoint Configuration

APP_NAME = "ib_comments"
OPERATION_NAME = "vote_a_comment"
REQUEST_METHOD = "post"
URL_SUFFIX = "vote_a_comment/"


from .test_case_01 import TestCase01VoteACommentAPITestCase

__all__ = [
    "TestCase01VoteACommentAPITestCase"
]


