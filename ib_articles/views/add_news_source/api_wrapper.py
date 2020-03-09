def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]

    url = request_data["url"]
    name = request_data["name"]

    from ib_articles.models import UserSuggestedNewsSource
    return UserSuggestedNewsSource.add_news_source(user, name, url)
