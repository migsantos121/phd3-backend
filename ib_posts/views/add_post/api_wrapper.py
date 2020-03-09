def api_wrapper(*args, **kwargs):
    request_data = kwargs['request_data']
    user = kwargs['user']

    from ib_posts.models.post import Post
    response_object = Post.add_post(request_data['content'], request_data['article_id'], user,
                                    request_data['multimedia_type'],
                                    request_data['multimedia_url'])
    return response_object