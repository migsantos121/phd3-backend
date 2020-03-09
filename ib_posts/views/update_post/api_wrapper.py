def api_wrapper(*args, **kwargs):
    request_data = kwargs['request_data']
    user = kwargs['user']
    post_id = kwargs['post_id']

    from ib_posts.models.post import Post
    Post.update_post(request_data['content'], post_id, request_data['article_id'], user)
    return