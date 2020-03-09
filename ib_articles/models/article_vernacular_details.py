from django.db import models
from ib_common.models.abstract_language_model import AbstractLanguageModel


class ArticleVernacularDetails(AbstractLanguageModel):
    article = models.ForeignKey('ib_articles.Article', related_name='vernacular_details')

    v_title = models.CharField(max_length=500)
    v_url = models.CharField(max_length=600)
    v_summary = models.TextField(max_length=100000000)
    v_author_name = models.CharField(max_length=300)
    v_published_time = models.DateTimeField(null=True)
    v_tags = models.TextField(max_length=1000, null=True, blank=True)
    v_image = models.CharField(max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return unicode("%s - %s" % (self.id, self.v_title))

    class Meta:
        app_label = "ib_articles"
        unique_together = (("article", 'language_name'),)
