def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    is_blocked = request_data["is_blocked"]
    access_token = kwargs["access_token"]

    from ib_recommender.adapters.service_adapter import ServiceAdapter
    _adapter = ServiceAdapter(user, access_token)

    from ib_recommender.models import UserKeywordMap
    return UserKeywordMap.get_user_keywords(user_id=user.id, is_blocked=is_blocked, _adapter=_adapter)
