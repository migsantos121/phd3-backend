def get_relations_response(request_object, user, source):
    m_id = request_object['m_id']
    m_type = request_object['m_type']
    relation_types = request_object['relation_types']
    r_m_types = request_object["r_m_types"]
    from ib_social.models.member_relation import MemberRelation
    response_object = MemberRelation.get_relations(relation_types=relation_types, source=source,
                                                   m_id=m_id, m_type=m_type, r_m_types=r_m_types)
    return response_object