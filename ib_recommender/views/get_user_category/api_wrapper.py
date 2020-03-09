def api_wrapper(*args, **kwargs):
    access_token = kwargs["access_token"]
    category_id = kwargs["category_id"]
    user = kwargs["user"]

    from ib_recommender.adapters.service_adapter import ServiceAdapter
    _adapter = ServiceAdapter(user, access_token)

    from ib_recommender.models import UserCategoryMap
    response_list = UserCategoryMap.get_user_categories(user=user, _adapter=_adapter, category_ids=[category_id])

    if not response_list:
        from django_swagger_utils.drf_server.exceptions.not_found import NotFound
        raise NotFound("Category Id not found")
    return response_list[0]
