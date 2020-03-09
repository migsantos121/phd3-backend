def api_wrapper(request_data, user, source):

    r_m_id = request_data['r_m_id']
    r_m_type = request_data['r_m_type']
    relation_types = request_data['relation_types']
    m_types = request_data["m_types"]
    status = request_data.get('status', 'ACCEPT')

    from ib_social.models.member_relation import MemberRelation
    response_object = MemberRelation.get_inverse_relations(relation_types, r_m_id, r_m_type, m_types, status, source)
    return response_object
