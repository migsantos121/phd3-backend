def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    access_token = kwargs["access_token"]

    offset = request_data["offset"]
    limit = request_data["limit"]
    category_ids = request_data["category_ids"]
    keyword_ids = request_data["keyword_ids"]

    from phd3.adapters.service_adapter import ServiceAdapter
    _adapter = ServiceAdapter(user, access_token)

    article_ids_list = _adapter.ib_recommender.get_articles(keyword_ids=keyword_ids, category_ids=category_ids)
    article_ids = [each["article_id"] for each in article_ids_list]

    from phd3.utils.article import Article
    articles = Article.get_articles(article_ids, _adapter, offset, limit)

    return articles


