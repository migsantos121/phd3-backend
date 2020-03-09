from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel

from ib_comments.models.comments import Comment


class UserCommentVote(AbstractDateTimeModel):
    COMMENT_CHOICES = (
        ('UP_VOTE', 'UP_VOTE'),
        ('DOWN_VOTE', 'DOWN_VOTE'),
        ('NEUTRAL', 'NEUTRAL'),
    )

    user_id = models.IntegerField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    vote = models.CharField(max_length=30, choices=COMMENT_CHOICES)

    def __unicode__(self):
        return unicode("%d-%s-%s" % (self.id, self.user_id, self.comment))

    class Meta:
        unique_together = ('user_id', 'comment',)

    @staticmethod
    def vote_a_comment(entity_id, entity_type, comment_id, vote, user, access_token=None):
        try:
            comment = Comment.objects.get(entity_id=entity_id, entity_type=entity_type, id=comment_id)
        except:
            general_error = {
                "error_code": 400,
                "error_remarks": "Given Comment Id is Doesn't Exist"
            }
            return general_error

        user_vote_object = list(UserCommentVote.objects.filter(comment=comment, user_id=user.id))

        if vote == "UP_VOTE":
            if len(user_vote_object) != 0 and user_vote_object[0].vote == "DOWN_VOTE":
                comment.up_votes += 1
                comment.down_votes -= 1
                user_vote_object[0].vote = vote
            elif len(user_vote_object) != 0 and user_vote_object[0].vote == "NEUTRAL":
                comment.up_votes += 1
                user_vote_object[0].vote = vote
            elif len(user_vote_object) != 0 and user_vote_object[0].vote == "UP_VOTE":
                pass
            else:
                comment.up_votes += 1
                user_comment = UserCommentVote(user_id=user.id, comment=comment, vote=vote)
                user_comment.save()

        if vote == "DOWN_VOTE":
            if len(user_vote_object) != 0 and user_vote_object[0].vote == "UP_VOTE":
                comment.up_votes -= 1
                comment.down_votes += 1
                user_vote_object[0].vote = vote
            elif len(user_vote_object) != 0 and user_vote_object[0].vote == "NEUTRAL":
                comment.down_votes += 1
                user_vote_object[0].vote = vote
            elif len(user_vote_object) != 0 and user_vote_object[0].vote == "DOWN_VOTE":
                pass
            else:
                comment.down_votes += 1
                user_comment = UserCommentVote(user_id=user.id, comment=comment, vote=vote)
                user_comment.save()

        elif vote == "NEUTRAL":
            if len(user_vote_object) != 0 and user_vote_object[0].vote == "UP_VOTE":
                comment.up_votes -= 1
                user_vote_object[0].vote = vote
            elif len(user_vote_object) != 0 and user_vote_object[0].vote == "NEUTRAL":
                pass
            elif len(user_vote_object) != 0 and user_vote_object[0].vote == "DOWN_VOTE":
                comment.down_votes -= 1
                user_vote_object[0].vote = vote
            else:
                user_comment = UserCommentVote(user_id=user.id, comment=comment, vote=vote)
                user_comment.save()

        else:
            pass

        if len(user_vote_object) != 0:
            user_vote_object[0].save()
        comment.save()

        from ib_users.interfaces.CommonInterface import CommonInterface
        from django.conf import settings
        interface_obj = CommonInterface(user=user, access_token=access_token,
                                        request_type=settings.IB_USERS_REQUEST_TYPE)
        user_object = interface_obj.get_user_details_by_id([comment.user_id])

        comment_details = {
            "entity_id": entity_id,
            "entity_type": entity_type,
            "comment_id": comment.id,
            "comment": comment.comment,
            "up_votes": comment.up_votes,
            "down_votes": comment.down_votes,
            "multimedia_url": comment.multimedia_url,
            "multimedia_type": comment.multimedia_type,
            "user_id": user_object[0]["m_id"],
            "username": user_object[0]["m_name"],
            "user_thumbnail_url": user_object[0]["m_pic_thumbnail"]
        }

        callback_dict = {'user_id': user.id, 'entity_id': comment.entity_id,
                         'entity_type': comment.entity_type, 'comment_id': comment.id,
                         'access_token': access_token, 'comment': comment.comment,
                         'sender_id':user.id, 'receiver_id':comment.user_id,
                         'username': user.username,
                         'user_thumbnail_url': user.pic_thumbnail}

        return comment_details, callback_dict
