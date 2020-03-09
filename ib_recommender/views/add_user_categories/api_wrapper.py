def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    category = request_data["category"]

    from ib_recommender.models import Category
    response_object = Category.add_category(user, category)
    return response_object
