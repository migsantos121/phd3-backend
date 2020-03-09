"""
Write your test case description here
"""

from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case \
    import CustomAPITestCase


REQUEST_BODY = """
{
    "search_q": "string", 
    "keyword_ids": [
        1
    ], 
    "category_ids": [
        1
    ], 
    "limit": 1, 
    "offset": 1
}
"""

RESPONSE_BODY = """
[
    {
        "published_time": "string", 
        "tags": "string", 
        "url": "string", 
        "title": "string", 
        "image_name": "string", 
        "author_name": "string", 
        "summary": "string", 
        "article_id": 1
    }
]
"""

TEST_CASE = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["read"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "type": "oauth2"}},
        "body": REQUEST_BODY,
    },
    "response": {
        "status": 200,
        "body": RESPONSE_BODY,
        "header_params": {}
    }
}


class TestCase01SearchUserArticlesAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
        super(TestCase01SearchUserArticlesAPITestCase, self). \
            __init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, 
                     TEST_CASE, *args, **kwargs)

    def test_case(self):
        response = super(TestCase01SearchUserArticlesAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


