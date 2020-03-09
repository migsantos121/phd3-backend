def api_wrapper(*args, **kwargs):
    request_data = kwargs['request_data']
    request_data["user"] = kwargs["user"]
    request_data["access_token"] = kwargs["access_token"]
    from ib_posts.models.post import Post
    response_object = Post.get_posts(**request_data)
    return response_object
