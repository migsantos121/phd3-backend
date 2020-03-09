from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel

from .new_source import NewsSource
from .category import Category


class RSSFeed(AbstractDateTimeModel):
    url = models.URLField(max_length=500)
    category = models.ForeignKey(Category)
    news_source = models.ForeignKey(NewsSource)

    def __unicode__(self):
        return unicode(self.url)

    class Meta:
        unique_together = ("url", 'category', 'news_source')
