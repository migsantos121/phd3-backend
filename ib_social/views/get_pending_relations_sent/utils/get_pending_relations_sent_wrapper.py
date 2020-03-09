"""
Created on 05/05/17

@author: revanth
"""


def get_pending_relations_sent_wrapper(request_data, user, access_token, source):
    m_id = request_data['m_id']
    m_type = request_data['m_type']
    relation_types = request_data['relation_types']
    limit = request_data['limit']
    offset = request_data['offset']

    from ib_social.models import MemberRelation
    friends_list, total_count = MemberRelation.get_pending_relations_sent(m_id=m_id, m_type=m_type, limit=limit,
                                                                          user=user, offset=offset,
                                                                          source=source,
                                                                          relation_types=relation_types,
                                                                          access_token=access_token)
    return {'count': total_count, 'friends': friends_list}

