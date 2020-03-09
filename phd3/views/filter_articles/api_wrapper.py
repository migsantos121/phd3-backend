def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    access_token = kwargs["access_token"]

    from phd3.adapters.service_adapter import ServiceAdapter
    _adapter = ServiceAdapter(user, access_token)

    offset = request_data["offset"]
    limit = request_data["limit"]
    is_bookmarked = request_data.get("is_bookmarked", False)
    is_liked = request_data.get("is_liked", False)
    is_shared = request_data.get("is_shared", False)
    articles = []
    article_ids = []

    if is_bookmarked:
        from phd3.utils.constants import SIPTHOR_ACTION_SOURCE, SIPTHOR_ACTION_ARTICLES
        actions = _adapter.ib_actions.get_user_actions_entities(
            offset=offset, limit=limit, source=SIPTHOR_ACTION_SOURCE,
            entity_types=[SIPTHOR_ACTION_ARTICLES],
            action_types=["BOOKMARK"],
            action_values=["BOOKMARK"]
        )
        article_ids = [each["entity_id"] for each in actions]

    if is_liked:
        from phd3.utils.constants import SIPTHOR_ACTION_SOURCE, SIPTHOR_ACTION_ARTICLES
        actions = _adapter.ib_actions.get_user_actions_entities(
            offset=offset, limit=limit, source=SIPTHOR_ACTION_SOURCE,
            entity_types=[SIPTHOR_ACTION_ARTICLES],
            action_types=["LIKE"],
            action_values=["LIKE"]
        )
        article_ids = [each["entity_id"] for each in actions]

    if is_shared:
        from phd3.utils.constants import SIPTHOR_ACTION_SOURCE, SIPTHOR_ACTION_ARTICLES
        actions = _adapter.ib_actions.get_user_actions_entities(
            offset=offset, limit=limit, source=SIPTHOR_ACTION_SOURCE,
            entity_types=[SIPTHOR_ACTION_ARTICLES],
            action_types=["SHARE"],
            action_values=[]
        )
        article_ids = [each["entity_id"] for each in actions]

    if article_ids:
        from phd3.utils.article import Article
        articles = Article.get_articles(article_ids, _adapter, offset, limit)

    return articles
