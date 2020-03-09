from django.db import models
from django.db.models.query_utils import Q
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel

from ib_notifications.constants.cloud_type import GROUP_TYPE, GroupType

__author__ = 'tanmay.ibhubs'


class NotificationGroup(AbstractDateTimeModel):
    group_name = models.CharField(max_length=50, null=True)
    group_type = models.CharField(max_length=50, null=False, choices=GROUP_TYPE, default=GroupType.GENERAL.value)
    source = models.CharField(max_length=300, null=False, default='')
    entity_id = models.IntegerField(null=False, default=-1)
    entity_type = models.CharField(null=False, default='', max_length=50)

    def __unicode__(self):
        return self.group_name

    class Meta:
        unique_together = (('entity_id', 'entity_type', 'source'),)
        app_label = 'ib_notifications'

    def convert_to_dict(self):
        user_ids = list(self.group_members.all().values_list('user_id', flat=True))
        return {
            "group_id": self.id,
            "group_name": self.group_name,
            "group_type": self.group_type,
            "user_ids": user_ids,
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "source": self.source
        }

    @classmethod
    def get_or_create_group_by_entity(cls, entity_id=None, entity_type=None, group_name=None, group_type=None,
                                      source=None,
                                      user=None,
                                      access_token=None):

        try:
            group = cls.objects.prefetch_related('group_members').get(entity_id=entity_id,
                                                                      entity_type=entity_type,
                                                                      source=source)
        except cls.DoesNotExist:
            group = cls.objects.create(entity_id=entity_id,
                                       entity_type=entity_type,
                                       group_name=group_name,
                                       group_type=group_type,
                                       source=source)

        return group

    @classmethod
    def get_group_by_entity(cls, entity_id=None, entity_type=None,
                                      source=None,
                                      user=None,
                                      access_token=None):

        try:
            group = cls.objects.prefetch_related('group_members').get(entity_id=entity_id,
                                                                      entity_type=entity_type,
                                                                      source=source)
        except cls.DoesNotExist:
            from django_swagger_utils.drf_server.exceptions.not_found import NotFound
            raise NotFound('Group not found for given entity')
        return group

    @classmethod
    def get_groups(cls, offset=None, limit=None, source=None, group_type=None, user=None, access_token=None):
        query = Q(source=source)
        if group_type:
            query &= Q(group_type=group_type)

        groups = cls.objects.prefetch_related('group_members').filter(query)
        total = groups.count()
        if limit == -1:
            limit = total
        elif not limit:
            limit = 10

        if not offset:
            offset = 0

        groups = groups[offset: offset + limit]
        groups_dict = [group.conver_to_dict() for group in groups]
        return {
            "total": total,
            "groups": groups_dict
        }
