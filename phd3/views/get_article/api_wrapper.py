def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    article_id = kwargs["article_id"]
    access_token = kwargs["access_token"]

    from phd3.adapters.service_adapter import ServiceAdapter
    _adapter = ServiceAdapter(user, access_token)

    article = _adapter.ib_articles.get_article(article_id)

    from phd3.utils.article import Article

    actions_summaries_dict = Article.get_actions_summaries_dict([article_id], _adapter)
    actions_summary = actions_summaries_dict[article_id]
    _dict = Article.get_action_summary_dict(actions_summary)

    comments_count_dict = Article.get_comments_dict([article_id], _adapter)
    comments_count = comments_count_dict.get(article_id, 0)
    _dict["comments_count"] = comments_count
    article.update({"action_summary": _dict})
    return article
