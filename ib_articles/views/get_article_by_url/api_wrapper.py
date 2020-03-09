def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    url = request_data["url"]

    from ib_articles.models import Article
    response = Article.get_article_by_url(user, url)
    return response
