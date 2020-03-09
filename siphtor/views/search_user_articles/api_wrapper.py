def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    access_token = kwargs["access_token"]

    search_q = request_data["search_q"]
    offset = request_data.get("offset", 0)
    limit = request_data.get("limit", 10)
    
    from phd3.adapters.service_adapter import ServiceAdapter
    _adapter = ServiceAdapter(user, access_token)

    users = _adapter.ib_articles.get_articles(search_q=search_q, offset=offset, limit=limit)
    return users
