def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    access_token = kwargs["access_token"]

    offset = request_data["offset"]
    limit = request_data["limit"]
    is_liked = request_data["is_liked"]
    is_shared = request_data.get("is_shared", False)

    from phd3.adapters.service_adapter import ServiceAdapter
    _adapter = ServiceAdapter(user, access_token)

    posts = []
    posts_ids = []

    if is_liked:
        from phd3.utils.constants import SIPTHOR_ACTION_SOURCE, SIPTHOR_ACTION_POSTS
        actions = _adapter.ib_actions.get_user_actions_entities(
            offset=offset, limit=limit, source=SIPTHOR_ACTION_SOURCE,
            entity_types=[SIPTHOR_ACTION_POSTS],
            action_types=["LIKE"],
            action_values=["LIKE"]
        )
        posts_ids = [each["entity_id"] for each in actions]

    if is_shared:
        from phd3.utils.constants import SIPTHOR_ACTION_SOURCE, SIPTHOR_ACTION_POSTS
        actions = _adapter.ib_actions.get_user_actions_entities(
            offset=offset, limit=limit, source=SIPTHOR_ACTION_SOURCE,
            entity_types=[SIPTHOR_ACTION_POSTS],
            action_types=["SHARE"],
            action_values=[]
        )
        posts_ids = [each["entity_id"] for each in actions]

    if posts_ids:
        posts = _adapter.ib_posts.get_posts(post_ids=posts_ids, user_ids=[], offset=offset, limit=limit)

    from phd3.utils.post import Post
    return Post.get_posts(posts, _adapter)
