from django.db import models
from ib_common.models.abstract_language_model import AbstractLanguageModel


class KeywordVernacularDetails(AbstractLanguageModel):
    keyword = models.ForeignKey('ib_articles.Keyword', related_name='vernacular_details')
    v_keyword = models.CharField(max_length=300)

    def __unicode__(self):
        return unicode("%s - %s" % (self.id, self.v_keyword))

    class Meta:
        app_label = "ib_articles"
        unique_together = (("keyword", 'language_name'),)
