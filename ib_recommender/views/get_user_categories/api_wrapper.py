def api_wrapper(*args, **kwargs):

    access_token = kwargs["access_token"]
    user = kwargs["user"]

    from ib_recommender.adapters.service_adapter import ServiceAdapter
    _adapter = ServiceAdapter(user, access_token)

    from ib_recommender.models import UserCategoryMap
    return UserCategoryMap.get_user_categories(user=user, _adapter=_adapter)
