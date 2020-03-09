def api_wrapper(*args, **kwargs):
    access_token = kwargs["access_token"]
    user = kwargs["user"]

    request_data = kwargs["request_data"]
    search_q = request_data["search_q"]
    offset = request_data.get("offset", 0)
    limit = request_data.get("limit", 0)

    from ib_recommender.adapters.service_adapter import ServiceAdapter
    _adapter = ServiceAdapter(user, access_token)

    keywords_list = _adapter.ib_articles.get_keywords(keyword_ids=[], search_q=search_q, limit=limit, offset=offset)
    return keywords_list
