def api_wrapper(*args, **kwargs):
    request_data = kwargs['request_data']
    user = kwargs['user']

    offset = request_data.get('offset', None)
    limit = request_data.get('limit', None)
    search_q = request_data.get('search_q', None)
    filters = request_data.get('filters', {})
    sorts = filters.get('sorts', None)
    article_ids = filters.get('article_ids', [])
    print article_ids
    published_time = sorts.get('published_time', None)

    from ib_articles.models.article import Article
    response_object = Article.get_article_by_ids(user, article_ids, offset, limit, published_time, search_q)

    return response_object
