from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "entity_id": 1,
    "entity_type": "article",
    "action_types": ["LIKE", "RATE", "BOOKMARK", "SUBSCRIBE", "SHARE", "FOLLOW", "ATTEND", "REPORT", "HELPFUL", "BOOK_STATUS", "BOOK_PROGRESS"],
    "source": "SOURCE1"
}
"""

response_body = """
{
    "subscribe_summary": {
        "positive": 0
    },
    "like_summary": {
        "positive": 0,
        "negative": 1
    },
    "rating_summary": [
        {
            "r_count": 0,
            "r_value": 0
        },
        {
            "r_count": 0,
            "r_value": 1
        },
        {
            "r_count": 0,
            "r_value": 2
        },
        {
            "r_count": 0,
            "r_value": 3
        },
        {
            "r_count": 0,
            "r_value": 4
        },
        {
            "r_count": 0,
            "r_value": 5
        },
        {
            "r_count": 0,
            "r_value": 6
        },
        {
            "r_count": 0,
            "r_value": 7
        },
        {
            "r_count": 0,
            "r_value": 8
        },
        {
            "r_count": 0,
            "r_value": 9
        },
        {
            "r_count": 1,
            "r_value": 10
        }
    ],
    "share_summary": {
        "positive": 0
    },
    "bookmark_summary": {
        "positive": 0
    },
    "follow_summary": {
        "positive": 0
    },
    "user_actions": [
        {
            "action_value": "10",
            "action_type": "RATE"
        },
        {
            "action_value": "DISLIKE",
            "action_type": "LIKE"
        },
        {
            "action_value": "NEUTRAL",
            "action_type": "VOTE"
        },
        {
            "action_value": "NEUTRAL",
            "action_type": "LOVE"
        },
        {
            "action_value": "NEUTRAL",
            "action_type": "SHARE"
        },
        {
            "action_value": "NEUTRAL",
            "action_type": "FOLLOW"
        },
        {
            "action_value": "NEUTRAL",
            "action_type": "BOOKMARK"
        },
        {
            "action_value": "NEUTRAL",
            "action_type": "FAVOURITE"
        },
        {
            "action_value": "NEUTRAL",
            "action_type": "SUBSCRIBE"
        }
    ]
}
"""

test_case = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["user read write"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01GetActionsSummaryAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetActionsSummaryAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase01GetActionsSummaryAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)

    def setupUser(self, username, password):
        super(TestCase01GetActionsSummaryAPITestCase, self).setupUser(username, password)

        from ib_action.models import Action
        Action.objects.create(action_value="10", source="SOURCE1", entity_id=1, action_type="RATE",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="LOVE", source="SOURCE1", entity_id=1, action_type="LOVE",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="WANT_TO_READ", source="SOURCE1", entity_id=1, action_type="BOOK_STATUS",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="READ", source="SOURCE1", entity_id=1, action_type="BOOK_STATUS",
                              entity_type="article", user_id=2)

        Action.objects.create(action_value="STARTED_READING", source="SOURCE1", entity_id=1, action_type="BOOK_STATUS",
                              entity_type="article", user_id=3)

        Action.objects.create(action_value="DISLIKE", source="SOURCE1", entity_id=1, action_type="LIKE",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="FAVOURITE", source="SOURCE1", entity_id=1, action_type="FAVOURITE",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="ATTEND", source="SOURCE1", entity_id=1, action_type="ATTEND",
                              entity_type="article", user_id=self.foo_user.id)