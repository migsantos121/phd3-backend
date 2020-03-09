def friends_with_relation_response(request_object, user, access_token, source=''):
    r_m_id = request_object['r_m_id']
    r_m_type = request_object['r_m_type']
    relation = request_object['relation']
    limit = request_object['limit']
    offset = request_object['offset']

    from ib_social.models import MemberRelation
    friends_list, member_friends_count, total_relations_count, has_relation = MemberRelation.get_friends_with_relation(
        r_m_id=r_m_id, r_m_type=r_m_type, limit=limit, offset=offset, relation=relation,
        user=user, access_token=access_token, source=source)
    return {'member_friends_count': member_friends_count,
            'friends': friends_list,
            'total_relation_count': total_relations_count,
            'has_relation': has_relation}
