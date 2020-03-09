def api_wrapper(*args, **kwargs):
    post_id = kwargs['post_id']
    user = kwargs['user']
    from ib_posts.models.post import Post
    response_object = Post.get_post_by_id(post_id=post_id, user=user)
    return response_object



