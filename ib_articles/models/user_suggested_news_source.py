from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel

from ib_articles.models import NewsSource


class UserSuggestedNewsSource(AbstractDateTimeModel):
    user_id = models.IntegerField()
    news_source = models.ForeignKey(NewsSource)

    class Meta:
        unique_together = ('user_id', 'news_source')

    def __unicode__(self):
        return unicode("%s %s" % (self.user_id, self.news_source))

    @classmethod
    def add_news_source(cls, user, name, url):
        from .new_source import NewsSource
        news_source, created = NewsSource.objects.get_or_create(name=name, url=url)
        if created:
            cls.objects.create(user_id=user.id, news_source=news_source)
        return {"news_source_id": news_source.id}
