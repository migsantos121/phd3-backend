from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """

"""

response_body = """

"""

test_case = {
    "request": {
        "path_params": {"post_id": "1"},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["write"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01DeletePostAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01DeletePostAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):
        from ib_posts.models.post import Post
        post = Post.objects.create(_contents='apple is not a fruit.', article_id=1, user_id=1)

        response = super(TestCase01DeletePostAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)

    def setupUser(self, username, password):
        super(TestCase01DeletePostAPITestCase, self).setupUser(username, password)

        self.foo_user.first_name = "user"
        self.foo_user.save()


