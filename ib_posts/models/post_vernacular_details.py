from django.db import models
from ib_common.models.abstract_language_model import AbstractLanguageModel

from ib_posts.constants.variables import MEDIA_TYPE


class PostVernacularDetails(AbstractLanguageModel):
    post = models.ForeignKey('ib_posts.Post', related_name='vernacular_details')
    v_contents = models.CharField(max_length=500)
    v_multimedia_url = models.CharField(max_length=500, null=True, blank=True)
    v_multimedia_type = models.CharField(max_length=200, null=True, blank=True, choices=MEDIA_TYPE)
    def __unicode__(self):
        return unicode("%s - %s" % (self.id, self.v_contents))

    class Meta:
        app_label = "ib_posts"
        unique_together = (("post", 'language_name'),)
