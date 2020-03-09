def get_pending_relation_requests_response(request_object, user, access_token, source):
    m_id = request_object['m_id']
    m_type = request_object['m_type']
    relation_types = request_object['relation_types']
    limit = request_object['limit']
    offset = request_object['offset']

    from ib_social.models import MemberRelation
    friends_list, total_count = MemberRelation.get_pending_relation_requests(m_id=m_id, m_type=m_type, limit=limit,
                                                                             user=user, offset=offset,
                                                                             source=source,
                                                                             relation_types=relation_types,
                                                                             access_token=access_token)
    return {'count': total_count, 'friends': friends_list}
