from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import CustomAPITestCase

request_body = """
{
    "m_id": 1, 
    "relation_types": [
        "FRIEND", 
        "FB_FRIEND"
    ],
    "r_m_types": [
        "r_m_type"
    ],
    "m_type": "m_type"
}
"""

response_body = """
[
    {
        "r_m_id": 2,
        "relation": "FRIEND",
        "r_m_type": "r_m_type"
    }
]
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


class TestCase02GetRelationsAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase02GetRelationsAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, test_case,
                                                  *args, **kwargs)

    def test_case(self):

        from ib_social.models.member_relation import MemberRelation
        member_object, is_created = MemberRelation.objects.get_or_create(m_id=1,
                                                             m_type="m_type",
                                                             r_m_id=2,
                                                             r_m_type="r_m_type")
        print member_object
        member_object.relation = "FRIEND"
        member_object.save()

        member_object, is_created = MemberRelation.objects.get_or_create(m_id=1,
                                                             m_type="m_type",
                                                             r_m_id=3,
                                                             r_m_type="r_m_type2")
        print member_object
        member_object.relation = "FB_FRIEND"
        member_object.save()

        member_object, is_created = MemberRelation.objects.get_or_create(m_id=1,
                                                             m_type="m_type",
                                                             r_m_id=4,
                                                             r_m_type="r_m_type3")
        print member_object
        member_object.relation = "FOLLOW"
        member_object.save()

        response = super(TestCase02GetRelationsAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)


