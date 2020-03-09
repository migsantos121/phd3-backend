from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "search_q": "str", 
    "keyword_ids": [
        1
    ]
}
"""

response_body = """
[{"keyword_id": 1, "keyword": "string"}]
"""

test_case = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["read"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01GetKeywordsAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetKeywordsAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):


        from ib_articles.models import Keyword, KeywordVernacularDetails, KeywordGroup

        keyword_group = KeywordGroup.objects.create(
            group="group",
            sub_group="sub_group",
            group_weight=0.1
        )
        keyword = Keyword.objects.create(_keyword="string", keyword_group=keyword_group)
        KeywordVernacularDetails.objects.create(v_keyword="string", keyword=keyword)

        response = super(TestCase01GetKeywordsAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


