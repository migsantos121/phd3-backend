def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]

    article_ids = request_data["article_ids"]
    sorts = request_data["sorts"]
    sort_by_published_date = sorts.get("published_time", "")

    published_time = request_data["published_time"]
    start_published_time = published_time.get("start_date_time", "")
    end_published_time = published_time.get("end_date_time", "")

    from ib_articles.models import Article
    articles = Article.get_basic_articles(
        user=user,
        article_ids=article_ids,
        sort_by_published_date=sort_by_published_date,
        end_published_time=end_published_time,
        start_published_time=start_published_time
    )
    return articles
