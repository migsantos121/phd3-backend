import django.dispatch

friends_searched = django.dispatch.Signal()


def get_friends_list_response(request_object, user, access_token, source=''):
    m_id = request_object['m_id']
    m_type = request_object['m_type']
    search_q = request_object['search_q']
    limit = request_object['limit']
    offset = request_object['offset']

    from ib_social.models import MemberRelation
    friends_list, total_count, callback_dict = MemberRelation.get_friends_list(m_id=m_id, m_type=m_type, limit=limit,
                                                                               user=user, access_token=access_token,
                                                                               offset=offset, search_q=search_q,
                                                                               source=source)
    if callback_dict:
        from ib_common.utilities.callback_wrapper import callback_wrapper
        callback_wrapper(source, 'ib_social', 'get_friends_list', access_token, 1, callback_dict,
                         friends_searched, user)
    return {'count': total_count, 'friends': friends_list}
