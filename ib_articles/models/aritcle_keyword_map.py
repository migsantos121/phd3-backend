from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel

from ib_articles.models.article import Article
from ib_articles.models.keyword import Keyword


class ArticleKeywordMap(AbstractDateTimeModel):
    article = models.ForeignKey(Article)
    keyword = models.ForeignKey(Keyword)
    relevance = models.FloatField()

    class Meta:
        unique_together = ('article', 'keyword')

    def __unicode__(self):
        return unicode("%s %s" % (self.article, self.keyword))

    @classmethod
    def get_article_keyword_maps(cls, keyword_ids):
        keyword_maps = cls.objects.filter(keyword_id__in=keyword_ids).values(
            'keyword__keyword_group__group',
            'keyword__keyword_group__sub_group',
            'keyword__keyword_group__group_weight',
            'article_id',
            'relevance',
            'keyword_id'
        )

        keyword_maps_list = []
        for each in keyword_maps:
            _dict = {
                "relevance": each['relevance'],
                "keyword_id": each['keyword_id'],
                "article_id": each['article_id'],
                "keyword_group": {
                    "group_weight": each['keyword__keyword_group__group_weight'],
                    "sub_group": each['keyword__keyword_group__sub_group'],
                    "group": each['keyword__keyword_group__group']
                }
            }
            keyword_maps_list.append(_dict)

        return keyword_maps_list
