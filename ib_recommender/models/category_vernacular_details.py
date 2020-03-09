from django.db import models
from ib_common.models.abstract_language_model import AbstractLanguageModel

from .category import Category


class CategoryVernacularDetails(AbstractLanguageModel):
    category = models.ForeignKey(Category, related_name='vernacular_details')
    v_category = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode("%s - %s" % (self.id, self.v_category))

    class Meta:
        unique_together = (("category", 'language_name'),)
