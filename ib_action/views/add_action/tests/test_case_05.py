from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "action_value": "1T0",
    "source": "SOURCE1",
    "entity_id": 1, 
    "action_type": "RATE",
    "entity_type": "article"
}
"""

response_body = """
{"res_status": "Action value is not an integer", "response": {}, "http_status_code": 417}
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
        "status": 417,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase05AddActionAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase05AddActionAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):

        response = super(TestCase05AddActionAPITestCase, self).test_case()
        # your extended implementation of test case

    def setupUser(self, username, password):
        super(TestCase05AddActionAPITestCase, self).setupUser(username, password)

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


