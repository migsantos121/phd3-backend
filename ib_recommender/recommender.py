class Recommender(object):
    def __init__(self, user_id=None, access_token=None, user=None, keyword_ids=None, category_ids=None):

        self.access_token = access_token
        if user is None:
            self.user = self.get_user_obj()
        else:
            self.user = user
        if user_id is None:
            self.user_id = user.id
        else:
            self.user_id = user_id
        self.keyword_ids = keyword_ids if keyword_ids is not None else []
        self.category_ids = category_ids if category_ids is not None else []

    @property
    def conn(self):
        from ib_recommender.adapters.service_adapter import ServiceAdapter
        service_adapter = ServiceAdapter(self.user, self.access_token)
        return service_adapter

    def get_user_obj(self):
        from django.contrib.auth import get_user_model
        user = get_user_model()
        try:
            user_obj = user.objects.get(id=self.user_id)
            return user_obj
        except user.DoesNotExist:
            return

    def get_category_keyword_ids(self):

        keyword_ids = []
        if self.category_ids:
            from ib_recommender.models import UserKeywordMap
            keyword_ids = list(UserKeywordMap.objects.filter(
                user_id=self.user_id,
                user_category_map__category_id__in=self.category_ids,
                is_blocked=False
            ).values_list('keyword_id', flat=True))
        return keyword_ids

    def get_user_keywords(self):

        from ib_recommender.models import UserKeywordMap
        user_keyword_maps = UserKeywordMap.objects.filter(user_id=self.user_id, is_blocked=False)

        filter_keyword_ids = self.keyword_ids
        filter_keyword_ids.extend(self.get_category_keyword_ids())
        if filter_keyword_ids:
            user_keyword_maps = user_keyword_maps.filter(keyword_id__in=filter_keyword_ids)
        user_keyword_maps = user_keyword_maps.values(
            'user_id',
            'keyword_id',
            'interest_score'
        )
        return user_keyword_maps

    def get_recommendations(self):

        user_key_words = self.get_user_keywords()
        article_relevance = self.get_mapped_articles_with_score_of_user(user_key_words)
        article_recency_dict = self.calculate_recency_score_all_articles()

        from django.conf import settings
        recency_default_score = settings.RECENCY_SCORE_INTERVAL / float(24 * settings.RECENCY_SCORE_DAYS)

        for article_id, relevance in article_relevance.items():
            article_relevance[article_id] = relevance * article_recency_dict.get(article_id, recency_default_score)

        recommendations = sorted(article_relevance.items(), key=lambda x: x[1], reverse=True)
        recommendations_list = []
        for each in recommendations:
            article_id, score = each
            _dict = {
                "cluster_ids": [],
                "article_id": article_id
            }
            recommendations_list.append(_dict)
        return recommendations_list

    def get_mapped_articles_with_score_of_user(self, user_key_words):
        keyword_ids = [each['keyword_id'] for each in user_key_words]
        article_keyword_map = self.conn.ib_articles.get_article_article_keyword_maps(keyword_ids)
        article_relevance = {}
        for each_key_word in user_key_words:
            for each_article_keyword in article_keyword_map:
                if each_article_keyword["keyword_id"] == each_key_word["keyword_id"]:
                    r = float(each_key_word["interest_score"]) * float(each_article_keyword["relevance"]) * \
                        float(each_article_keyword["keyword_group"]["group_weight"])
                    if each_article_keyword["article_id"] in article_relevance:
                        article_relevance[each_article_keyword["article_id"]] += r
                    else:
                        article_relevance[each_article_keyword["article_id"]] = r
        return article_relevance

    def calculate_recency_score_all_articles(self):

        from datetime import datetime, timedelta
        from django.conf import settings

        start_date = datetime.now() - timedelta(days=settings.RECENCY_SCORE_DAYS)
        articles_list = self.conn.ib_articles.get_basic_articles(
            article_ids=[],
            start_published_time=start_date,
            end_published_time=datetime.now()
        )

        recency_interval = settings.RECENCY_SCORE_INTERVAL
        articles_recency_score_dict = {}
        for article in articles_list:
            difference_in_hours = ((datetime.now() - article['published_time'].replace(
                tzinfo=None)).total_seconds()) / 3600
            articles_recency_score_dict[article['article_id']] = (recency_interval / difference_in_hours)

        return articles_recency_score_dict
