def api_wrapper(*args, **kwargs):

    user = kwargs["user"]
    category_id = kwargs["category_id"]

    from ib_recommender.models import Category
    Category.remove_category(user, category_id)

    return

