def api_wrapper(*args, **kwargs):
    request_data = kwargs['request_data']
    user = kwargs['user']
    article_id = kwargs['article_id']

    title = request_data.get('title', None)
    summary = request_data.get('summary', None)
    url = request_data.get('url', None)

    author_name = request_data.get('author_name', None)
    published_time = request_data.get('published_time', None)
    tags = request_data.get('tags', None)
    image = request_data.get('image', None)
    news_source_id = request_data.get('news_source_id', None)

    from ib_articles.models.article import Article
    Article.update_article(user, article_id, title, summary, url, author_name, published_time, tags, image,
                           news_source_id)
    return
