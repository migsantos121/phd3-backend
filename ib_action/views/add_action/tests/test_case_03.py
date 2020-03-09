from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "action_value": "100",
    "source": "SOURCE1",
    "entity_id": 1, 
    "action_type": "BOOK_PROGRESS",
    "entity_type": "article"
}
"""

response_body = """
{
    "subscribe_summary": {
        "positive": 0
    },
    "like_summary": {
        "positive": 1,
        "negative": 0
    },
    "favourite_summary": {
        "positive": 1
    },
    "attend_summary": {
        "positive": 0
    },
    "helpful_summary": {
        "positive": 0
    },
    "vote_summary": {
        "positive": 1,
        "negative": 0
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
        "positive": 1
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
            "action_value": "LIKE",
            "action_type": "LIKE"
        },
        {
            "action_value": "UPVOTE",
            "action_type": "VOTE"
        },
        {
            "action_value": "LOVE",
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
            "action_value": "BOOKMARK",
            "action_type": "BOOKMARK"
        },
        {
            "action_value": "FAVOURITE",
            "action_type": "FAVOURITE"
        },
        {
            "action_value": "NEUTRAL",
            "action_type": "SUBSCRIBE"
        },
        {
            "action_value": "NEUTRAL",
            "action_type": "REPORT"
        },
        {
            "action_value": "NEUTRAL",
            "action_type": "HELPFUL"
        },
        {
            "action_value": "NEUTRAL",
            "action_type": "ATTEND"
        }
    ],
    "report_summary": {
        "positive": 0
    },
    "love_summary": {
        "positive": 1
    }
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


class TestCase03AddActionAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase03AddActionAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):

        response = super(TestCase03AddActionAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)

    def setupUser(self, username, password):
        super(TestCase03AddActionAPITestCase, self).setupUser(username, password)

        from ib_action.models import Action
        Action.objects.create(action_value="10", source="SOURCE1", entity_id=1, action_type="RATE",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="LOVE", source="SOURCE1", entity_id=1, action_type="LOVE",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="DISLIKE", source="SOURCE1", entity_id=1, action_type="LIKE",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="BOOKMARK", source="SOURCE1", entity_id=1, action_type="BOOKMARK",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="UPVOTE", source="SOURCE1", entity_id=1, action_type="VOTE",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="FAVOURITE", source="SOURCE1", entity_id=1, action_type="FAVOURITE",
                              entity_type="article", user_id=self.foo_user.id)


