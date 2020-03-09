def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    keyword_ids = request_data["keyword_ids"]
    search_q = request_data["search_q"]
    offset = request_data.get("offset", 0)
    limit = request_data.get("limit", 0)

    from ib_articles.models import Keyword
    return Keyword.get_keywords(user=user, keyword_ids=keyword_ids, search_q=search_q, limit=limit, offset=offset)
