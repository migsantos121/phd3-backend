def api_wrapper(*args, **kwargs):
    post_id = kwargs['post_id']
    user = kwargs['user']
    access_token = kwargs["access_token"]

    from ib_posts.adapters.service_adapter import ServiceAdapter
    _adapter = ServiceAdapter(user=user, access_token=access_token)

    from ib_posts.models.post import Post
    response_object = Post.get_post_by_id_with_article(post_id=post_id, user=user, _adapter=_adapter)

    return response_object
