import django.dispatch

connection_update = django.dispatch.Signal()


def update_relation_response(request_object, user, access_token, source):
    m_id = request_object['m_id']
    m_type = request_object['m_type']
    r_m_id = request_object['r_m_id']
    r_m_type = request_object['r_m_type']
    relation = request_object['relation']

    from ib_social.models.member_relation import MemberRelation
    relations, callback_dict = MemberRelation.update_member_relation(
        m_id=m_id, m_type=m_type, r_m_id=r_m_id, r_m_type=r_m_type, relation=relation, user=user, source=source)

    if callback_dict:
        from ib_common.utilities.callback_wrapper import callback_wrapper
        callback_wrapper(source, 'ib_social', 'update_relation', access_token, 1, callback_dict,
                         connection_update, user)

    return relations
