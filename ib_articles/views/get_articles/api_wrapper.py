def api_wrapper(*args, **kwargs):
    request_data = kwargs['request_data']
    user = kwargs['user']
    from ib_articles.models.article import Article
    if request_data['usage']:
        search_q = request_data['search_q']
        limit = request_data['limit']
        offset = request_data['offset']
        get_article = Article.get_article_news(search_q = search_q, offset = offset, limit = limit)
        return get_article
    else:
        offset = request_data.get('offset', None)
        limit = request_data.get('limit', None)
        search_q = request_data.get('search_q', None)
        filters = request_data.get('filters', {})
        sorts = filters.get('sorts', None)
        published_time = sorts.get('published_time', None)

        response_object = Article.get_articles(user, offset, limit, search_q, published_time)
        return response_object
