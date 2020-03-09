from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "source": "SOURCE1", 
    "offset": 0, 
    "limit": 10, 
    "action_type": "LIKE", 
    "entity_type": "article"
}
"""

response_body = """
{
    "total": 1, 
    "actions": [
        {
            "action_value": "DISLIKE", 
            "entity_id": 1, 
            "user_id": 1, 
            "entity_type": "article", 
            "source": "SOURCE1", 
            "action_type": "LIKE"
        }
    ]
}

"""

test_case = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["read", "write"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01GetUserActionEntitiesAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetUserActionEntitiesAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase01GetUserActionEntitiesAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)

    def setupUser(self, username, password):
        super(TestCase01GetUserActionEntitiesAPITestCase, self).setupUser(username, password)

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



