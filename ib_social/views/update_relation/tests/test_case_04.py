from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "r_m_id": 2,
    "m_id": 1, 
    "relation": "FOLLOW",
    "r_m_type": "r_m_type",
    "m_type": "m_type"
}
"""

response_body = """
"""

test_case = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {"oauth": {"scopes": ["read write"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password", "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase04UpdateRelationAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase04UpdateRelationAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX,
                                                                  test_case,
                                                                  *args, **kwargs)

    def test_case(self):
        response = super(TestCase04UpdateRelationAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)



        from ib_social.models.member_relation import MemberRelation
        print MemberRelation.objects.all()
        member_object = MemberRelation.objects.get(m_id=1,
                                                               m_type="m_type",
                                                               r_m_id=2,
                                                               r_m_type="r_m_type",
                                                               relation="FRIEND")
        self.assertEqual(1, member_object.id)

        from ib_social.models.member_relation import MemberRelation
        member_object = MemberRelation.objects.get(m_id=2,
                                                               m_type="r_m_type",
                                                               r_m_id=1,
                                                               r_m_type="m_type",
                                                               relation="FRIEND")
        self.assertEqual(2, member_object.id)
