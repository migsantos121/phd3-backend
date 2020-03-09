from django.db import models


class UserActionMap(models.Model):
    user_id = models.IntegerField()
    action_id = models.IntegerField()
    weight = models.FloatField()
    article_id = models.IntegerField()
    is_action_considered = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user_id', 'action_id', 'article_id')

    def __unicode__(self):
        return unicode("%s %s %s" % (self.user_id, self.article_id, self.action_id))
