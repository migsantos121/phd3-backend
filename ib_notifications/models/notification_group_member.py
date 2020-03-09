from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel

from ib_notifications.constants.cloud_type import GroupType

__author__ = 'tanmay.ibhubs'


class NotificationGroupMember(AbstractDateTimeModel):
    group = models.ForeignKey('ib_notifications.NotificationGroup', on_delete=models.CASCADE,
                              related_name="group_members")
    user_id = models.IntegerField(null=False, default=-1)

    class Meta:
        unique_together = (('group', 'user_id'),)
        app_label = 'ib_notifications'

    def __unicode__(self):
        return str(self.id)

    @classmethod
    def add_notification_group_member(cls, user_ids=None, entity_id=None, entity_type=None, group_name=None,
                                      group_type=GroupType.GENERAL.value, source=None, user=None,
                                      access_token=None):

        from ib_notifications.models.notification_group import NotificationGroup
        group = NotificationGroup.get_or_create_group_by_entity(entity_id, entity_type, group_name, group_type, source, user,
                                                                access_token)

        old_group_members = list(group.group_members.all().values_list('user_id', flat=True))
        user_ids_to_add = list(set(user_ids) - set(old_group_members))
        group_members = []
        for user_id in user_ids_to_add:
            group_members.append(cls(
                group=group,
                user_id=user_id
            ))

        cls.objects.bulk_create(group_members)
        return

    @classmethod
    def get_group_member_ids(cls, group_id=None, source=None, user=None, access_token=None):
        from ib_notifications.models.notification_group import NotificationGroup
        try:
            group = NotificationGroup.objects.get(id=group_id, source=source)
        except:
            from django_swagger_utils.drf_server.exceptions.not_found import NotFound
            raise NotFound('Group doesn\'t exists', res_status=False)

        group_member_ids = cls.objects.filter(group=group).values_list('user_id', flat=True)

        return list(group_member_ids)
