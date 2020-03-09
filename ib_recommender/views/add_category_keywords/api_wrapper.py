def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    category_id = kwargs["category_id"]
    request_data = kwargs["request_data"]
    keyword_ids = request_data["keyword_ids"]

    from ib_recommender.models import UserKeywordMap
    UserKeywordMap.add_user_keywords(user=user, keyword_ids=keyword_ids, category_id=category_id)
    return
