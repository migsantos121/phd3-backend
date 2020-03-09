def api_wrapper(*args, **kwargs):
    request_data = kwargs["request_data"]
    keyword_ids = request_data["keyword_ids"]

    from ib_articles.models import ArticleKeywordMap
    return ArticleKeywordMap.get_article_keyword_maps(keyword_ids)
