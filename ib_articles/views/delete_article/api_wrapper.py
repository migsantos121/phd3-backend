def api_wrapper(*args, **kwargs):
    article_id = kwargs['article_id']
    user = kwargs['user']

    from ib_articles.models.article import Article
    Article.delete_article(article_id, user)

    return
