def api_wrapper(*args, **kwargs):

    user = kwargs["user"]
    request_data = kwargs["request_data"]

    title = request_data['title']
    summary = request_data['summary']
    url = request_data['url']
    author_name = request_data['author_name']
    published_time = request_data['published_time']
    tags = request_data["tags"]
    image = request_data.get("image", None)
    news_source_id = request_data.get("news_source_id", None)

    from ib_articles.models.article import Article
    response_object = Article.add_article(title, summary, url, user, author_name, published_time, tags, image,
                                          news_source_id)
    return response_object
