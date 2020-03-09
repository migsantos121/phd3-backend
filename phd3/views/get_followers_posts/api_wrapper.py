def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    access_token = kwargs["access_token"]

    profile_user_id = request_data["profile_user_id"]
    offset = request_data["offset"]
    limit = request_data["limit"]
    # todo include friends shared post also in this api

    from phd3.adapters.service_adapter import ServiceAdapter
    _adapter = ServiceAdapter(user, access_token)

    from phd3.utils.constants import IB_SOCIAL_USER_TYPE, IB_SOCIAL_FOLLOW_TYPE
    following_users = _adapter.ib_social.get_relations(m_id=user.id, m_type=IB_SOCIAL_USER_TYPE,
                                                       relation_types=[IB_SOCIAL_FOLLOW_TYPE],
                                                       r_m_types=[IB_SOCIAL_USER_TYPE])
    following_user_ids = [each["r_m_id"] for each in following_users]
    if(profile_user_id == ''):
        posts = _adapter.ib_posts.get_posts(post_ids=[], user_ids=following_user_ids, offset=offset, limit=limit)
    else:
        posts = _adapter.ib_posts.get_posts(post_ids=[], user_ids=profile_user_id, offset=offset, limit=limit)
    from phd3.utils.post import Post
    return Post.get_posts(posts, _adapter)
