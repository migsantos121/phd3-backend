def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    access_token = kwargs["access_token"]

    offset = request_data["offset"]
    limit = request_data["limit"]

    media_types = request_data.get("media_types", [])

    from phd3.adapters.service_adapter import ServiceAdapter
    _adapter = ServiceAdapter(user, access_token)
    posts = _adapter.ib_posts.get_user_posts(offset, limit, media_types)

    from phd3.utils.post import Post
    return Post.get_posts(posts, _adapter)
