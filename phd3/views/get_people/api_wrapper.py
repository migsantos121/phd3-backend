def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    access_token = kwargs["access_token"]

    offset = request_data["offset"]
    limit = request_data["limit"]
    relation = request_data["relation"]

    from phd3.adapters.service_adapter import ServiceAdapter
    _adapter = ServiceAdapter(user, access_token)

    user_ids = []

    from phd3.utils.constants import IB_SOCIAL_USER_TYPE, IB_SOCIAL_FOLLOW_TYPE, IB_SOCIAL_FOLLOWING_TYPE

    if relation == IB_SOCIAL_FOLLOWING_TYPE:
        following_users = _adapter.ib_social.get_relations(m_id=user.id, m_type=IB_SOCIAL_USER_TYPE,
                                                           relation_types=[IB_SOCIAL_FOLLOW_TYPE],
                                                           r_m_types=[IB_SOCIAL_USER_TYPE])
        user_ids = [each["r_m_id"] for each in following_users]
    elif relation == IB_SOCIAL_FOLLOW_TYPE:
        follower_users = _adapter.ib_social.get_inverse_relations(r_m_id=user.id, r_m_type=IB_SOCIAL_USER_TYPE,
                                                                  relation_types=[IB_SOCIAL_FOLLOW_TYPE],
                                                                  m_types=[IB_SOCIAL_USER_TYPE])
        user_ids = [each["m_id"] for each in follower_users]

    entities = []
    for each_id in user_ids:
        _entity = {
            "m_id": each_id,
            "relation_types": [
                IB_SOCIAL_FOLLOW_TYPE
            ],
            "m_type": IB_SOCIAL_USER_TYPE
        }
        entities.append(_entity)

    users_dict = dict()
    users = _adapter.ib_users.get_users(user_ids=user_ids, search_q="", exclude_user_ids=[])
    for each_user in users:
        users_dict[each_user["user_id"]] = each_user

    stats_list = []
    if entities:
        stats_list = _adapter.ib_social.get_relations_stats(request_data=entities)

    from phd3.utils.constants import RELATED_RELATIONS
    people = []
    for each_stat in stats_list:
        _dict = dict()
        _dict['user_info'] = users_dict.get(each_stat["m_id"], {})
        _dict["counts"] = []
        for each in each_stat["user_relations_count"]:
            _dict["counts"].append({"relation": each["relation_val"], "relation_count": each["relation_count"]})
        for each in each_stat["related_users_count"]:
            _dict["counts"].append(
                {"relation": RELATED_RELATIONS[each["relation_val"]], "relation_count": each["relation_count"]})
        people.append(_dict)

    people = people[offset: offset + limit]
    return people
