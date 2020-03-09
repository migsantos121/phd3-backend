def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    keyword_ids = request_data["keyword_ids"]
    category_ids = request_data["category_ids"]
    from ib_recommender.recommender import Recommender
    recommender = Recommender(user=user, keyword_ids=keyword_ids, category_ids=category_ids)
    return recommender.get_recommendations()