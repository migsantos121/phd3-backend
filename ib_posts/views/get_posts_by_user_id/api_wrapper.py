def api_wrapper(*args, **kwargs):
    request_data = kwargs['request_data']
    request_data["user"] = kwargs["user"]
    request_data["access_token"] = kwargs["access_token"]

    filters = request_data.get("filters", {})
    filters.update({"user_ids": [kwargs["user"].id]})
    request_data["filters"] = filters

    from ib_posts.models.post import Post
    response_object = Post.get_posts(**request_data)
    return response_object
