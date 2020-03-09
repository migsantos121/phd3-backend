class Article(object):
    @classmethod
    def get_action_summary_dict(cls, actions_summary):
        if not actions_summary["users_actions_summaries"]:
            return {
                "like_summary": {
                    "positive": 0,
                    "negative": 0
                },
                "bookmark_summary": {
                    "positive": 0,
                },
                "share_summary": {
                    "positive": 0,
                },
                "is_bookmarked": False,
                "is_shared": False,
                "is_liked": False,
                "is_disliked": False,
            }
        user_action_summary = actions_summary["users_actions_summaries"][0]["user_actions"]
        user_action_summary_dict = dict()
        for each_action in user_action_summary:
            user_action_summary_dict[each_action["action_type"]] = each_action["action_value"]
        _dict = dict()
        _dict["like_summary"] = actions_summary["like_summary"]
        _dict["bookmark_summary"] = actions_summary["bookmark_summary"]
        _dict["share_summary"] = actions_summary["share_summary"]
        _dict["is_bookmarked"] = "BOOKMARK" in user_action_summary_dict.keys() and user_action_summary_dict.get("BOOKMARK") != "NEUTRAL"
        _dict["is_shared"] = "SHARE" in user_action_summary_dict.keys() and user_action_summary_dict.get("SHARE") != "NEUTRAL"
        _dict["is_liked"] = "LIKE" in user_action_summary_dict.keys() and user_action_summary_dict.get("LIKE") == "LIKE"
        _dict["is_disliked"] = "LIKE" in user_action_summary_dict.keys() and user_action_summary_dict.get("LIKE") == "DISLIKE"
        return _dict

    @classmethod
    def get_entities(cls, article_ids):
        from phd3.utils.constants import SIPTHOR_ACTION_ARTICLES
        entities = []
        for each_id in article_ids:
            _dict = {
                "entity_id": each_id,
                "entity_type": SIPTHOR_ACTION_ARTICLES
            }
            entities.append(_dict)
        return entities

    @classmethod
    def get_actions_summaries_dict(cls, article_ids, _adapter):
        from phd3.utils.constants import SIPTHOR_ACTION_SOURCE
        entities = cls.get_entities(article_ids)

        action_type_filters = [
            "LIKE",
            "BOOKMARK",
            "SHARE"
        ]
        actions_summaries = _adapter.ib_actions.get_users_actions_summaries(
            entities=entities,
            source=SIPTHOR_ACTION_SOURCE,
            user_ids=[],
            action_type_filters=action_type_filters
        )

        actions_summaries_dict = dict()
        for each in actions_summaries:
            actions_summaries_dict[each["entity_id"]] = each
        return actions_summaries_dict

    @classmethod
    def get_comments_dict(cls, article_ids, _adapter):
        entities = cls.get_entities(article_ids)
        comment_count_list = _adapter.ib_comments.get_count_of_comments(entities)
        comment_count_dict = dict()
        for each in comment_count_list:
            comment_count_dict[each["entity_id"]] = each["comments_count"]
        return comment_count_dict

    @classmethod
    def get_articles(cls, article_ids, _adapter, offset, limit):
        articles = []
        if article_ids:
            articles = _adapter.ib_articles.get_article_by_ids(article_ids, offset, limit)

        article_ids = [each["article_id"] for each in articles]

        actions_summaries_dict = cls.get_actions_summaries_dict(article_ids, _adapter)
        # print actions_summaries_dict
        comments_count_dict = cls.get_comments_dict(article_ids, _adapter)
        for each_article in articles:
            actions_summary = actions_summaries_dict[each_article["article_id"]]
            _dict = cls.get_action_summary_dict(actions_summary)

            comments_count = comments_count_dict.get(each_article["article_id"], 0)
            _dict["comments_count"] = comments_count
            each_article.update({"action_summary": _dict})

        return articles