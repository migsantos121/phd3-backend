def update_relation_status_response(request_object, user, access_token, source):
    m_id = request_object['m_id']
    m_type = request_object['m_type']
    r_m_id = request_object['r_m_id']
    r_m_type = request_object['r_m_type']
    relation = request_object['relation']
    status = request_object['status']

    from ib_social.models.member_relation import MemberRelation
    relations, callback_dict = MemberRelation.update_member_relation_status(source=source,
        m_id=m_id, m_type=m_type, r_m_id=r_m_id, r_m_type=r_m_type, relation=relation, user=user, status=status)

    if callback_dict:
        from ib_common.utilities.callback_wrapper import callback_wrapper
        from ib_social.views.update_relation.utils.update_relation_response import connection_update
        callback_wrapper(source, 'ib_social', 'update_relation', access_token, 1, callback_dict,
                         connection_update, user)

    return relations
