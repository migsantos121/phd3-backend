from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "entities": [
        {
            "entity_id": 1,
            "entity_type": "article"
        },
        {
            "entity_id": 2,
            "entity_type": "article"
        },
        {
            "entity_id": 3,
            "entity_type": "article"
        }
    ],
    "action_types": [
        "RATE",
        "LOVE",
        "LIKE",
        "BOOKMARK",
        "ATTEND",
        "REPORT",
        "HELPFUL"
    ], 
    "user_ids": [
        1, 
        2,
        3
    ], 
    "source": "SOURCE1"
}
"""

response_body = """
[
    {
        "entity_id": 1,
        "entity_type": "article",
        "users_actions_summaries": [
            {
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
                        "action_value": "NEUTRAL",
                        "action_type": "FAVOURITE"
                    },
                    {
                        "action_value": "NEUTRAL",
                        "action_type": "SUBSCRIBE"
                    }
                ],
                "user_id": 1
            },
            {
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
                ],
                "user_id": 2
            },
            {
                "user_actions": [
                    {
                        "action_value": "NEUTRAL",
                        "action_type": "RATE"
                    },
                    {
                        "action_value": "NEUTRAL",
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
                        "action_value": "BOOKMARK",
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
                ],
                "user_id": 3
            }
        ],
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
        "bookmark_summary": {
            "positive": 1
        },
        "like_summary": {
            "positive": 0,
            "negative": 1
        },
        "love_summary": {
            "positive": 1
        }
    },
    {
        "entity_id": 2,
        "entity_type": "article",
        "users_actions_summaries": [
            {
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
                        "action_value": "NEUTRAL",
                        "action_type": "FAVOURITE"
                    },
                    {
                        "action_value": "NEUTRAL",
                        "action_type": "SUBSCRIBE"
                    }
                ],
                "user_id": 1
            },
            {
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
                ],
                "user_id": 2
            },
            {
                "user_actions": [
                    {
                        "action_value": "NEUTRAL",
                        "action_type": "RATE"
                    },
                    {
                        "action_value": "NEUTRAL",
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
                        "action_value": "BOOKMARK",
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
                ],
                "user_id": 3
            }
        ],
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
        "bookmark_summary": {
            "positive": 0
        },
        "like_summary": {
            "positive": 0,
            "negative": 1
        },
        "love_summary": {
            "positive": 1
        }
    },
    {
        "entity_id": 3,
        "entity_type": "article",
        "users_actions_summaries": [
            {
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
                        "action_value": "NEUTRAL",
                        "action_type": "FAVOURITE"
                    },
                    {
                        "action_value": "NEUTRAL",
                        "action_type": "SUBSCRIBE"
                    }
                ],
                "user_id": 1
            },
            {
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
                ],
                "user_id": 2
            },
            {
                "user_actions": [
                    {
                        "action_value": "NEUTRAL",
                        "action_type": "RATE"
                    },
                    {
                        "action_value": "NEUTRAL",
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
                        "action_value": "BOOKMARK",
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
                ],
                "user_id": 3
            }
        ],
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
                "r_count": 0,
                "r_value": 10
            }
        ],
        "bookmark_summary": {
            "positive": 1
        },
        "like_summary": {
            "positive": 0,
            "negative": 0
        },
        "love_summary": {
            "positive": 0
        }
    }
]
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


class TestCase01GetUsersActionsSummaryAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetUsersActionsSummaryAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)


    def test_case(self):
        response = super(TestCase01GetUsersActionsSummaryAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


    def setupUser(self, username, password):
        super(TestCase01GetUsersActionsSummaryAPITestCase, self).setupUser(username, password)

        from ib_action.models import Action
        Action.objects.create(action_value="10", source="SOURCE1", entity_id=1, action_type="RATE",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="LOVE", source="SOURCE1", entity_id=1, action_type="LOVE",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="DISLIKE", source="SOURCE1", entity_id=1, action_type="LIKE",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="BOOKMARK", source="SOURCE1", entity_id=1, action_type="BOOKMARK",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="HELPFUL", source="SOURCE1", entity_id=1, action_type="HELPFUL",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="REPORT", source="SOURCE1", entity_id=1, action_type="REPORT",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="UPVOTE", source="SOURCE1", entity_id=1, action_type="VOTE",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="FAVOURITE", source="SOURCE1", entity_id=1, action_type="FAVOURITE",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="ATTEND", source="SOURCE1", entity_id=1, action_type="ATTEND",
                              entity_type="article", user_id=self.foo_user.id)

        Action.objects.create(action_value="10", source="SOURCE1", entity_id=2, action_type="RATE",
                              entity_type="article", user_id=2)

        Action.objects.create(action_value="LOVE", source="SOURCE1", entity_id=2, action_type="LOVE",
                              entity_type="article", user_id=2)

        Action.objects.create(action_value="DISLIKE", source="SOURCE1", entity_id=2, action_type="LIKE",
                              entity_type="article", user_id=2)

        Action.objects.create(action_value="BOOKMARK", source="SOURCE1", entity_id=3, action_type="BOOKMARK",
                              entity_type="article", user_id=3)

        Action.objects.create(action_value="UPVOTE", source="SOURCE1", entity_id=3, action_type="VOTE",
                              entity_type="article", user_id=3)

        Action.objects.create(action_value="FAVOURITE", source="SOURCE1", entity_id=3, action_type="FAVOURITE",
                              entity_type="article", user_id=3)

