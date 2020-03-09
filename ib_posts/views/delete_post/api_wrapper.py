def api_wrapper(*args, **kwargs):
    post_id = kwargs['post_id']
    user = kwargs['user']

    from ib_posts.models.post import Post
    Post.delete_post(post_id=post_id, user=user)
    return