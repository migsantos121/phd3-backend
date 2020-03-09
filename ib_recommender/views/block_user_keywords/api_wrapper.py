def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    keyword_ids = request_data["keyword_ids"]

    from ib_recommender.models import UserKeywordMap
    UserKeywordMap.block_user_keywords(user=user, keyword_ids=keyword_ids, is_blocked=True)

    return
