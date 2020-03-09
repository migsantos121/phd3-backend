def api_wrapper(*args, **kwargs):
    """


    :param args:
    :param kwargs:
    :return:
    """

    response = {
        "articles": {
            "is_disliked": 0,
            "is_liked": 0,
            "total": 0,
            "is_bookmarked": 0,
            "is_shared": 0
        },
        "posts": {
            "is_disliked": 0,
            "is_liked": 0,
            "total": 0,
            "is_bookmarked": 0,
            "is_shared": 0
        },
        "social_counts": [],
        "posts_media_type": []
    }

    user = kwargs["user"]
    access_token = kwargs["access_token"]

    from phd3.adapters.service_adapter import ServiceAdapter
    _adapter = ServiceAdapter(user, access_token)

    from phd3.utils import constants
    like_bookmark_actions = _adapter.ib_actions.user_action_counts(
        source=constants.SIPTHOR_ACTION_SOURCE,
        entity_types=[constants.SIPTHOR_ACTION_ARTICLES, constants.SIPTHOR_ACTION_POSTS],
        action_types=[constants.SIPTHOR_ACTION_BOOKMARK, constants.SIPTHOR_ACTION_LIKE],
        action_values=[constants.SIPTHOR_ACTION_BOOKMARK, constants.SIPTHOR_ACTION_LIKE,
                       constants.SIPTHOR_ACTION_DISLIKE]
    )

    for each_action in like_bookmark_actions:
        if each_action["entity_id"] in [-1, 0]:
            continue
        if each_action['action_type'] == constants.SIPTHOR_ACTION_BOOKMARK:
            response[each_action['entity_type']]["is_bookmarked"] += each_action['entity_count']
        if each_action['action_type'] == constants.SIPTHOR_ACTION_LIKE:
            if each_action['action_value'] == constants.SIPTHOR_ACTION_LIKE:
                response[each_action['entity_type']]["is_liked"] += each_action['entity_count']
            if each_action['action_value'] == constants.SIPTHOR_ACTION_DISLIKE:
                response[each_action['entity_type']]["is_disliked"] += each_action['entity_count']

    share_actions = _adapter.ib_actions.user_action_counts(
        source=constants.SIPTHOR_ACTION_SOURCE,
        entity_types=[constants.SIPTHOR_ACTION_ARTICLES, constants.SIPTHOR_ACTION_POSTS],
        action_types=[constants.SIPTHOR_ACTION_SHARE],
        action_values=[]
    )

    for each_action in share_actions:
        if each_action["entity_id"] in [-1, 0]:
            continue
        if each_action['action_type'] == constants.SIPTHOR_ACTION_SHARE:
            response[each_action['entity_type']]["is_shared"] += each_action['entity_count']

    posts_stats = _adapter.ib_posts.get_post_user_stats()
    response[constants.SIPTHOR_ACTION_POSTS]["total"] = posts_stats["total"]
    response["posts_media_type"] = []
    for each in posts_stats["posts_media_type"]:
        if each["multimedia_type"] is not None and each["multimedia_type"]:
            each["media_type"] = each["multimedia_type"].upper()
            response["posts_media_type"].append(each)
    _entity = {
        "m_id": user.id,
        "relation_types": [
            constants.IB_SOCIAL_FOLLOW_TYPE
        ],
        "m_type": constants.IB_SOCIAL_USER_TYPE
    }
    stats_list = _adapter.ib_social.get_relations_stats(request_data=[_entity])
    stats_list = stats_list[0]
    for each in stats_list["user_relations_count"]:
        each["relation"] = each["relation_val"]
    response["social_counts"] = []
    if stats_list["user_relations_count"]:
        _following = stats_list["user_relations_count"][0]
        _following["relation"] = constants.IB_SOCIAL_FOLLOWING_TYPE
        response["social_counts"].append(_following)
    if stats_list["related_users_count"]:
        _follow = stats_list["related_users_count"][0]
        _follow["relation"] = constants.IB_SOCIAL_FOLLOW_TYPE
        response["social_counts"].append(_follow)
    return response
