from django.db import models
from django.db.models.query_utils import Q
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel


class Comment(AbstractDateTimeModel):
    entity_id = models.IntegerField()
    entity_type = models.CharField(max_length=100)
    user_id = models.IntegerField()
    comment = models.TextField()
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    multimedia_url = models.CharField(max_length=500, null=True, blank=True)
    multimedia_type = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return unicode("%d-%s-%s" % (self.id, self.entity_type, self.multimedia_type))

    @classmethod
    def delete_comment(cls, user_id, comment_id):
        try:
            comment = cls.objects.get(user_id=user_id, id=comment_id)
            comment.delete()
        except cls.DoesNotExist:
            from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed
            raise ExpectationFailed({}, res_status="comment not exist/not permitted to current user")
        from django.http import HttpResponse
        return HttpResponse()

    @staticmethod
    def comment_on_entity(entity_id, entity_type, comment, multimedia, multimedia_type, user, access_token, source=''):

        comment = Comment(entity_id=entity_id, user_id=user.id, entity_type=entity_type, comment=comment,
                          multimedia_url=multimedia, multimedia_type=multimedia_type)
        comment.save()

        from ib_users.interfaces.CommonInterface import CommonInterface
        from django.conf import settings

        interface_obj = CommonInterface(user=user, access_token=access_token,
                                        request_type=settings.IB_USERS_REQUEST_TYPE)

        user_object = interface_obj.get_user_details_by_id([user.id])

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
            "user_thumbnail_url": user_object[0].get("m_pic_thumbnail", '')
        }

        receivers_id = list(
            Comment.objects.filter(entity_id=comment.entity_id, entity_type='COMMENT').distinct().values_list('user_id',
                                                                                                              flat=True))
        if entity_id != -1:
            try:
                parent_comment = Comment.objects.get(id=entity_id)
                receivers_id.append(parent_comment.user_id)
            except Comment.DoesNotExist:
                pass
        if user.id in receivers_id:
            receivers_id.remove(user.id)

        callback_dict = {'username': user_object[0]['m_username'],
                         "receivers_id": receivers_id,
                         "sender_id": user.id, "access_token": access_token}
        extra_data = {"user_id": user_object[0]["m_id"],
                      "comment": comment.comment, "comment_id": comment.id,
                      "entity_id": comment.entity_id,
                      "entity_type": comment.entity_type,
                      "user_thumbnail_url": user_object[0]["m_pic_thumbnail"], }
        callback_dict.update(extra_data)

        return comment_details, callback_dict

    @staticmethod
    def get_list_of_comments(entity_id, entity_type, offset, limit, user, access_token, search_q=None):

        query = Q(entity_id=entity_id, entity_type=entity_type)

        if search_q:
            query &= Q(comment__contains=search_q)
        comments_query_set = Comment.objects.filter(query).order_by('-creation_datetime')
        total = comments_query_set.count()
        comments_list = list(comments_query_set[offset:offset + limit])
        if comments_list:
            print comments_list
            user_ids_map = dict()
            comment_ids = []
            for each_item in comments_list:
                comment_ids.append(each_item.id)
                user_ids_map[each_item.id] = each_item.user_id

            from ib_users.interfaces.CommonInterface import CommonInterface
            from django.conf import settings
            interface_obj = CommonInterface(user=user, access_token=access_token,
                                            request_type=settings.IB_USERS_REQUEST_TYPE)
            comments_details = []

            user_objects = interface_obj.get_user_details_by_id(user_ids_map.values())

            user_details_map = dict()
            for each_user_details in user_objects:
                user_details_map[each_user_details['m_id']] = each_user_details

            # count comment on top comments
            from django.db.models import Count
            comments_count = list(
                Comment.objects.filter(entity_id__in=comment_ids, entity_type='COMMENT').values('entity_id',
                                                                                                'entity_type').annotate(
                    comments_count=Count('entity_id')))
            print "Comments_Count ========>", comments_count
            if not comments_count:
                comments_count = []

            comment_count_dict = {}
            for comment_count in comments_count:
                comment_count_dict[comment_count['entity_id']] = comment_count.get('comments_count', 0)

            print "Comments_Count_Dict ========>", comment_count_dict

            # made a dictionary like {1:1,2:1,:3:2}

            for each_comment in comments_list:
                each_user_id = user_ids_map[each_comment.id]
                user_object = user_details_map[each_user_id]
                comment_count = comment_count_dict.get(each_comment.id, 0)
                comment = {
                    "comment_id": each_comment.id,
                    "comment": each_comment.comment,
                    "up_votes": each_comment.up_votes,
                    "down_votes": each_comment.down_votes,
                    "multimedia_url": each_comment.multimedia_url,
                    "multimedia_type": each_comment.multimedia_type,
                    "user_id": user_object["m_id"],
                    "comments_count": comment_count,
                    "username": user_object["m_name"],
                    "user_thumbnail_url": user_object["m_pic_thumbnail"],
                    "created_on": each_comment.creation_datetime
                }
                comments_details.append(comment)

            list_of_comments = {
                "entity_id": comments_list[0].entity_id,
                "entity_type": comments_list[0].entity_type,
                "comments": comments_details,
                "total": total
            }
            return list_of_comments
        else:
            list_of_comments = {
                "entity_id": entity_id,
                "entity_type": entity_type,
                "comments": []
            }
            return list_of_comments

    @staticmethod
    def get_count_of_comments(entity_id, entity_type):
        comments_list = Comment.objects.filter(entity_id=entity_id, entity_type=entity_type).count()

        comments_count = {
            "entity_id": entity_id,
            "entity_type": entity_type,
            "comments_count": comments_list
        }
        return comments_count

    @staticmethod
    def get_counts_of_comments(entity_ids, entity_types):
        from django.db.models import Count
        return list(Comment.objects.filter(entity_id__in=entity_ids, entity_type__in=entity_types)
                    .values('entity_id', 'entity_type')
                    .annotate(comments_count=Count('entity_id', ))
                    .values('comments_count', 'entity_id', 'entity_type'))
