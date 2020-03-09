def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    access_token = kwargs["access_token"]

    search_q = request_data["search_q"]
    offset = request_data.get("offset", 0)
    limit = request_data.get("limit", 10)

    from phd3.adapters.service_adapter import ServiceAdapter
    _adapter = ServiceAdapter(user, access_token)

    from phd3.utils.constants import IB_SOCIAL_USER_TYPE, IB_SOCIAL_FOLLOW_TYPE
    following_users = _adapter.ib_social.get_relations(m_id=user.id, m_type=IB_SOCIAL_USER_TYPE,
                                                       relation_types=[IB_SOCIAL_FOLLOW_TYPE],
                                                       r_m_types=[IB_SOCIAL_USER_TYPE])

    following_user_ids = [ each["r_m_id"] for each in following_users]
    following_user_ids.append(user.id)
    users = _adapter.ib_users.get_users(user_ids=[], search_q=search_q, exclude_user_ids=following_user_ids, offset=offset, limit=limit)
    return users


