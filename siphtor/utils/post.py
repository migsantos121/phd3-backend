class Post(object):
    @classmethod
    def get_entities(cls, post_ids):
        from phd3.utils.constants import SIPTHOR_ACTION_POSTS
        entities = []
        for each_id in post_ids:
            _dict = {
                "entity_id": each_id,
                "entity_type": SIPTHOR_ACTION_POSTS
            }
            entities.append(_dict)
        return entities

    @classmethod
    def get_posts(cls, posts, _adapter):
        post_ids, article_ids = [], []
        for each_post in posts:
            post_ids.append(each_post["post_id"])
            if each_post["article_id"] and each_post["article_id"] != -1:
                article_ids.append(each_post["article_id"])

        article_actions_dict, posts_actions_dict = cls.get_posts_actions_dict(post_ids, article_ids, _adapter)
        articles_comment_count_dict, posts_comment_count_dict = cls.get_comments_counts_dict(
            post_ids, article_ids, _adapter)

        from phd3.utils.article import Article
        for each_post in posts:

            article_id = each_post["article_id"]
            if article_id and article_id != -1:
                article_action_summary = article_actions_dict[each_post["article_id"]]
                article_dict = Article.get_action_summary_dict(article_action_summary)
                article_comments_count = articles_comment_count_dict.get(each_post["article_id"], 0)
                article_dict["comments_count"] = article_comments_count
                each_post["article_info"].update({"action_summary": article_dict})

            actions_summary = posts_actions_dict[each_post["post_id"]]
            _dict = Article.get_action_summary_dict(actions_summary)
            comments_count = posts_comment_count_dict.get(each_post["post_id"], 0)
            _dict["comments_count"] = comments_count
            each_post.update({"action_summary": _dict})

        return posts

    @classmethod
    def get_comments_counts_dict(cls, post_ids, article_ids, _adapter):

        from .article import Article
        entities = Article.get_entities(article_ids)
        entities.extend(cls.get_entities(post_ids))

        comment_count_list = _adapter.ib_comments.get_count_of_comments(entities)
        articles_comment_count_dict, posts_comment_count_dict = dict(), dict()

        from phd3.utils.constants import SIPTHOR_ACTION_POSTS, SIPTHOR_ACTION_ARTICLES
        for each in comment_count_list:
            if each["entity_type"] == SIPTHOR_ACTION_POSTS:
                posts_comment_count_dict[each["entity_id"]] = each["comments_count"]
            elif each["entity_type"] == SIPTHOR_ACTION_ARTICLES:
                articles_comment_count_dict[each["entity_id"]] = each["comments_count"]
        return articles_comment_count_dict, posts_comment_count_dict

    @classmethod
    def get_posts_actions_dict(cls, post_ids, article_ids, _adapter):

        from .article import Article
        entities = Article.get_entities(article_ids)
        entities.extend(cls.get_entities(post_ids))

        action_type_filters = [
            "LIKE",
            "BOOKMARK",
            "SHARE"
        ]
        from phd3.utils.constants import SIPTHOR_ACTION_SOURCE, SIPTHOR_ACTION_POSTS, SIPTHOR_ACTION_ARTICLES
        actions_summaries = _adapter.ib_actions.get_users_actions_summaries(
            entities=entities,
            source=SIPTHOR_ACTION_SOURCE,
            user_ids=[],
            action_type_filters=action_type_filters
        )

        article_actions_dict, posts_actions_dict = dict(), dict()
        for each in actions_summaries:

            if each["entity_type"] == SIPTHOR_ACTION_POSTS:
                posts_actions_dict[each["entity_id"]] = each
            elif each["entity_type"] == SIPTHOR_ACTION_ARTICLES:
                article_actions_dict[each["entity_id"]] = each
        return article_actions_dict, posts_actions_dict
