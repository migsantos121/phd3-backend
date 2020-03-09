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
    ],
    "m_type": "USER"
}
"""

response_body = """
[
    {
        "r_m_id": 2,
        "relation": "FRIEND",
        "r_m_type": "USER"
    },
    {
        "r_m_id": 3,
        "relation": "FB_FRIEND",
        "r_m_type": "USER"
    }
]
"""

test_case = {
    "request": {
        "path_params": {},
        "query_params": {},
        "header_params": {},
        "securities": {
            "oauth": {"scopes": ["read write"], "tokenUrl": "http://auth.ibtspl.com/oauth2/", "flow": "password",
                      "type": "oauth2"}},
        "body": request_body,
    },
    "response": {
        "status": 200,
        "body": response_body,
        "header_params": {}
    }
}


class TestCase01GetRelationsAPITestCase(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase01GetRelationsAPITestCase, self).__init__(APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX,
                                                                test_case,
                                                                *args, **kwargs)

    def test_case(self):
        from ib_social.models.member_relation import MemberRelation
        member_object, is_created = MemberRelation.objects.get_or_create(m_id=1,
                                                                         m_type="USER",
                                                                         r_m_id=2,
                                                                         r_m_type="USER",
                                                                         status="ACCEPT")
        print member_object
        member_object.relation = "FRIEND"
        member_object.save()

        member_object, is_created = MemberRelation.objects.get_or_create(m_id=1,
                                                                         m_type="USER",
                                                                         r_m_id=3,
                                                                         r_m_type="USER",
                                                                         status="ACCEPT")
        print member_object
        member_object.relation = "FB_FRIEND"
        member_object.save()

        member_object, is_created = MemberRelation.objects.get_or_create(m_id=1,
                                                                         m_type="USER",
                                                                         r_m_id=4,
                                                                         r_m_type="USER",
                                                                         status="ACCEPT")
        print member_object
        member_object.relation = "FOLLOW"
        member_object.save()

        response = super(TestCase01GetRelationsAPITestCase, self).test_case()
        # your extended implementation of test case
        self.assertEqual(response.status_code, 200)
