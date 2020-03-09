from django.db import models
from ib_comments.models.comments import Comment
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel


class UserCommentReport(AbstractDateTimeModel):

    user_id = models.IntegerField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __unicode__(self):
        return unicode("%d-%s" % (self.id, self.user_id))

    class Meta:
        unique_together = ('user_id', 'comment')

    @staticmethod
    def report_a_comment(entity_id, entity_type, comment_id, user):
        try:
            comment = Comment.objects.get(entity_id=entity_id, entity_type=entity_type, id=comment_id)
        except:
            general_error = {
                "error_code": 400,
                "error_remarks": "Given Comment id is Doesn't Exist"
            }
            return general_error

        user_comment_report = UserCommentReport(user_id=user.id, comment=comment)
        user_comment_report.save()

        return
