import re

from django.db import models
from django_swagger_utils.drf_server.exceptions.not_found import NotFound
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel

from ib_social.constants.relation_types import RELATION_TYPES, NEGATIVE_RELATIONS, OPPOSITE_RELATION, RELATION_STATUSES
from ib_social.constants.relation_types import SYMMETRIC_RELATIONS
from ib_social.constants.variables import Variables, RelationshipStatus, Relations
from ib_social.utilities import get_friends_id_from_facebook, get_followers_ids_from_twitter

__author__ = 'tanmay.ibhubs'


class MemberRelationManager(models.Manager):
    def get_queryset(self):
        return super(MemberRelationManager, self).get_queryset().filter(is_deleted=False)


class MemberRelation(AbstractDateTimeModel):
    m_id = models.IntegerField()
    m_type = models.CharField(max_length=255)
    r_m_id = models.IntegerField()
    r_m_type = models.CharField(max_length=255)
    relation = models.CharField(choices=RELATION_TYPES, max_length=255, default='FRIEND')
    status = models.CharField(choices=RELATION_STATUSES, max_length=100, default='ACCEPT')
    m_social_id = models.CharField(null=True, max_length=100)
    is_deleted = models.BooleanField(null=False, default=False)
    source = models.CharField(max_length=100, default="")

    class Meta:
        app_label = 'ib_social'

    def __unicode__(self):
        return str(self.id)

    objects = MemberRelationManager()

    @staticmethod
    def get_friends_list_bulk(request_data, user, access_token, source):
        from django.db.models import Q
        request_m_query = Q()
        for each_req in request_data:
            each_req["m_id"] = user.id if each_req["m_type"] == "USER" and each_req["m_id"] == -1 else each_req["m_id"]
            request_m_query |= Q(m_id=each_req["m_id"], m_type=each_req["m_type"], source=source)

        related_friends_list = MemberRelation.objects.filter(request_m_query) \
            .filter(status="ACCEPT", relation__in=["FB_FRIEND", "FRIEND"]).values("m_id", "r_m_id", "r_m_type")

        friends_list_bulk_response = list()
        for each_req in request_data:
            each_req_user_friend_m_ids_list = list()
            for each_related_friend in related_friends_list:
                if each_req["m_id"] == each_related_friend["m_id"]:
                    each_req_user_friend_m_ids_list.append(each_related_friend)
            friends_list = MemberRelation.get_friends_details(access_token=access_token, user=user,
                                                              user_type="r_m_type", user_id_type="r_m_id",
                                                              member_friends_list=each_req_user_friend_m_ids_list)
            total_friends_count = len(friends_list)
            limit = each_req.get("limit", 0)
            offset = each_req.get("offset", 0)
            if limit > 0:
                friends_list = friends_list[offset: offset + limit]
            friends_list_bulk_response.append({
                'count': total_friends_count,
                'user_id': each_req["m_id"],
                'friends': friends_list
            })
        return friends_list_bulk_response

    @staticmethod
    def get_pending_relation_requests(m_id, m_type, limit, user, offset, relation_types, access_token, source):
        m_id = user.id if m_type == "USER" and m_id == -1 else m_id
        pending_relation_requests = MemberRelation.objects.filter(source=source,
                                                                  m_id=m_id, m_type=m_type,
                                                                  status="WAITING_FOR_APPROVAL").values("r_m_id",
                                                                                                        "r_m_type")
        if relation_types:
            pending_relation_requests = pending_relation_requests.filter(relation__in=relation_types)
        total_requests_count = len(pending_relation_requests)
        if total_requests_count == 0:
            return [], 0
        requested_friends_list = MemberRelation.get_friends_details(access_token=access_token, user=user,
                                                                    member_friends_list=pending_relation_requests,
                                                                    user_type="r_m_type", user_id_type="r_m_id")
        if limit > 0:
            requested_friends_list = requested_friends_list[offset: offset + limit]
        return requested_friends_list, total_requests_count

    @staticmethod
    def get_friends_with_relation(r_m_id, r_m_type, limit, offset, relation, user, access_token, source):
        total_relations = MemberRelation.objects.filter(r_m_id=r_m_id, r_m_type=r_m_type, relation=relation,
                                                        status="ACCEPT", source=source).values_list('m_id', 'm_type')
        has_relation = MemberRelation.check_has_relation(total_relations=total_relations, user=user)
        member_friends_count, member_friends_list = MemberRelation.get_members_list(r_m_id=r_m_id, r_m_type=r_m_type,
                                                                                    limit=limit, offset=offset,
                                                                                    relation=relation, user=user,
                                                                                    source=source)
        friends_list = MemberRelation.get_friends_details(access_token=access_token, user=user,
                                                          member_friends_list=member_friends_list)
        return friends_list, member_friends_count, len(total_relations), has_relation

    @classmethod
    def get_pending_relations_sent(cls, m_id, m_type, limit, user, offset, relation_types, access_token, source):
        m_id = user.id if m_type == "USER" and m_id == -1 else m_id
        pending_relations_sent = cls.objects.filter(m_id=m_id, m_type=m_type, status="PENDING", source=source). \
            values("r_m_id", "r_m_type")
        if relation_types:
            pending_relations_sent = pending_relations_sent.filter(relation__in=relation_types)
        total_requests_count = len(pending_relations_sent)
        if total_requests_count == 0:
            return [], 0
        requested_friends_list = MemberRelation.get_friends_details(access_token=access_token, user=user,
                                                                    member_friends_list=pending_relations_sent,
                                                                    user_type="r_m_type", user_id_type="r_m_id")
        if limit > 0:
            requested_friends_list = requested_friends_list[offset: offset + limit]
        return requested_friends_list, total_requests_count

    @classmethod
    def get_friends_details(cls, member_friends_list, user, access_token, user_type="m_type", user_id_type="m_id"):
        ib_user_ids = list()
        sh_users = list()
        for each_member_friend in member_friends_list:
            if each_member_friend[user_type] == "USER":
                ib_user_ids.append(each_member_friend[user_id_type])
            else:
                sh_users.append({
                    "user_id": each_member_friend[user_id_type],
                    "user_type": each_member_friend[user_type]
                })
        ib_users_friends_list = cls.get_ib_users_friends_details(user, access_token, ib_user_ids=ib_user_ids)
        sh_users_friends_list = cls.get_sh_users_friends_details(user, access_token, sh_users=sh_users)
        friends_list = ib_users_friends_list + sh_users_friends_list
        return friends_list

    @classmethod
    def get_sh_users_friends_details(cls, user, access_token, sh_users):
        friends_list = list()
        # todo : to get stakeholders objects in bulk need implementation in ib_connect
        for each_sh_user in sh_users:
            # from ib_social.adapters.get_stake_holder_adapter import get_stake_holder_adapter
            # ib_users_info = get_stake_holder_adapter(user=user, access_token=access_token,
            #                                          member_id=each_sh_user["user_id"],
            #                                          member_type=each_sh_user["user_type"])
            # friends_list.append({
            #     "user_id": ib_users_info["sh_id"],
            #     "user_name": ib_users_info["name"],
            #     "user_thumbnail": ib_users_info["thumbnail"]
            # })
            friends_list.append({
                "user_id": each_sh_user["user_id"],
                "user_name": "",
                "user_thumbnail": ""
            })
        return friends_list

    @classmethod
    def get_ib_users_friends_details(cls, user, access_token, ib_user_ids):
        from ib_social.adapters.get_users_info_adapter import get_users_info_adapter
        ib_users_info = get_users_info_adapter(user=user, access_token=access_token, user_ids=ib_user_ids)
        friends_list = list()
        for each_user_info in ib_users_info:
            friends_list.append({
                "user_id": each_user_info["m_id"],
                "user_name": each_user_info["m_name"],
                "user_thumbnail": each_user_info["m_pic_thumbnail"],
            })
        return friends_list

    @classmethod
    def get_members_list(cls, r_m_id, r_m_type, limit, offset, relation, user, source):
        current_user_related_m_ids_list = MemberRelation.objects.filter(
            m_id=user.id, status="ACCEPT", relation__in=["FB_FRIEND", "FRIEND"], source=source).\
            values_list("r_m_id", flat=True)

        member_friends_list = list(
            MemberRelation.objects.filter(r_m_id=r_m_id, r_m_type=r_m_type, relation=relation, status="ACCEPT",
                                          source=source,
                                          m_id__in=current_user_related_m_ids_list).distinct().values("m_id", "m_type"))

        member_friends_count = len(member_friends_list)
        if limit > 0:
            member_friends_list = member_friends_list[offset: offset + limit]
        return member_friends_count, member_friends_list

    @classmethod
    def check_has_relation(cls, total_relations, user):
        has_relation = False
        for each_relation in total_relations:
            if each_relation[0] == user.id and each_relation[1] == 'USER':
                has_relation = True
        return has_relation

    @staticmethod
    def get_friends_list(m_id, m_type, limit, offset, search_q, user, access_token, source):
        m_id = user.id if m_type == "USER" and m_id == -1 else m_id
        friends_m_ids_list = MemberRelation.objects.filter(m_id=m_id, m_type=m_type, status="ACCEPT", source=source,
                                                           relation__in=["FB_FRIEND", "FRIEND"]).values("r_m_id",
                                                                                                        "r_m_type")
        friends_list = MemberRelation.get_friends_details(access_token=access_token, user=user,
                                                          member_friends_list=friends_m_ids_list,
                                                          user_type="r_m_type", user_id_type="r_m_id")
        total_friends_count = len(friends_list)
        callback_dict = dict()
        if search_q:
            search_q_filtered_friends_list = list()
            for each_friend in friends_list:
                if each_friend["user_name"] and re.search(search_q, each_friend["user_name"], re.IGNORECASE):
                    search_q_filtered_friends_list.append(each_friend)
            friends_list = search_q_filtered_friends_list

            from ib_social.constants.resource_type import resource_type
            callback_dict["entity_type"] = resource_type["IB_SOCIAL_FRIENDS"]
            callback_dict['search_key'] = search_q

        if limit > 0:
            friends_list = friends_list[offset: offset + limit]
        return friends_list, total_friends_count, callback_dict

    @classmethod
    def update_member_relation(cls, m_id, m_type, r_m_id, r_m_type, relation, user, source):

        m_id = user.id if m_type == "USER" and m_id == -1 else m_id

        if m_id == r_m_id and m_type == r_m_type:
            from django_swagger_utils.drf_server.exceptions.bad_request import BadRequest
            raise BadRequest('A relation can\'t be established between same user')

        if relation in NEGATIVE_RELATIONS:
            relation = OPPOSITE_RELATION[relation]
            return cls.delete_relation(m_id, m_type, r_m_id, r_m_type, relation, user, source), {}

        if relation == "BLOCK":
            relations = OPPOSITE_RELATION[relation]
            cls.delete_all_relations(m_id, m_type, r_m_id, r_m_type, relations, user, source), {}

        cls.check_for_blocked_relations(m_id, m_type, r_m_id, r_m_type, user, source)
        member_relation_object, is_created = MemberRelation.objects.get_or_create(source=source,
                                                                                  m_id=m_id, m_type=m_type,
                                                                                  r_m_id=r_m_id, r_m_type=r_m_type,
                                                                                  relation=relation)

        if not is_created:
            from django_swagger_utils.drf_server.exceptions.bad_request import BadRequest
            raise BadRequest('Relation already exists, use update api')

        if relation in SYMMETRIC_RELATIONS:
            related_m_r_obj, is_created = MemberRelation.objects.get_or_create(source=source,
                                                                               m_id=r_m_id, m_type=r_m_type,
                                                                               status="WAITING_FOR_APPROVAL",
                                                                               r_m_id=m_id, r_m_type=m_type,
                                                                               relation=relation)
            if not is_created:
                member_relation_object.status = "ACCEPT"
                related_m_r_obj.status = "ACCEPT"
                related_m_r_obj.save()
            else:
                member_relation_object.status = "PENDING"
        else:
            member_relation_object.status = "ACCEPT"

        member_relation_object.save()
        callback_dict = {'user_id': member_relation_object.m_id, 'other_user_id': member_relation_object.r_m_id,
                         'relation': member_relation_object.relation, 'status': member_relation_object.status,
                         'is_symmetric': True if member_relation_object.relation in SYMMETRIC_RELATIONS else False}

        member_relations = list(
            MemberRelation.objects.filter(source=source, m_id=m_id, m_type=m_type, r_m_id=r_m_id, r_m_type=r_m_type).
                values('relation', 'status'))
        member_relations_info = list()
        for member_relation in member_relations:
            member_relations_info.append({'relation': str(member_relation["relation"]),
                                          'status': str(member_relation["status"])})
        return member_relations_info, callback_dict

    @classmethod
    def update_member_relation_status(cls, m_id, m_type, r_m_id, r_m_type, relation, user, status, source):
        m_id = user.id if m_type == "USER" and m_id == -1 else m_id

        if m_id == r_m_id and m_type == r_m_type:
            from django_swagger_utils.drf_server.exceptions.bad_request import BadRequest
            raise BadRequest('A relation can\'t be established between same user')

        if status == 'REJECT':
            return cls.delete_relation(m_id, m_type, r_m_id, r_m_type, relation, user, source), {}

        member_relation, is_created = MemberRelation.objects.get_or_create(source=source, m_id=m_id, m_type=m_type,
                                                                           r_m_id=r_m_id,
                                                                           r_m_type=r_m_type, relation=relation)
        if not is_created and member_relation.status == status:
            from django_swagger_utils.drf_server.exceptions.bad_request import BadRequest
            raise BadRequest('Relation already exists')
        member_relation.status = status
        member_relation.save()

        if relation in SYMMETRIC_RELATIONS:
            r_member_relation, is_created = MemberRelation.objects.get_or_create(source=source, m_id=r_m_id,
                                                                                 m_type=r_m_type, r_m_id=m_id,
                                                                                 r_m_type=m_type, relation=relation)
            r_member_relation.status = status
            r_member_relation.save()
        callback_dict = {'user_id': member_relation.m_id, 'other_user_id': member_relation.r_m_id,
                         'relation': member_relation.relation, 'status': member_relation.status,
                         'is_symmetric': True if member_relation.relation in SYMMETRIC_RELATIONS else False}

        member_relations = list(
            MemberRelation.objects.filter(source=source, m_id=m_id, m_type=m_type, r_m_id=r_m_id, r_m_type=r_m_type).
                values('relation', 'status'))
        member_relations_info = list()
        for member_relation in member_relations:
            member_relations_info.append({'relation': str(member_relation["relation"]),
                                          'status': str(member_relation["status"])})
        return member_relations_info, callback_dict

    @classmethod
    def check_for_blocked_relations(cls, m_id, m_type, r_m_id, r_m_type, user, source):
        m_id = user.id if m_type == "USER" and m_id == -1 else m_id

        from django.db.models import Q
        query = Q()
        query |= Q(m_id=m_id, m_type=m_type, r_m_id=r_m_id, r_m_type=r_m_type, source=source)
        query |= Q(m_id=r_m_id, m_type=r_m_type, r_m_id=m_id, r_m_type=m_type, source=source)
        member_relations = list(MemberRelation.objects.filter(query).values_list('relation', flat=True))

        if "BLOCK" in member_relations:
            from django_swagger_utils.drf_server.exceptions.bad_request import BadRequest
            raise BadRequest('Can not create relation')

    @classmethod
    def delete_all_relations(cls, m_id, m_type, r_m_id, r_m_type, relations, user, source):
        m_id = user.id if m_type == "USER" and m_id == -1 else m_id

        from django.db.models import Q
        query = Q()
        query |= Q(m_id=m_id, m_type=m_type, r_m_id=r_m_id, r_m_type=r_m_type, source=source)
        query |= Q(m_id=r_m_id, m_type=r_m_type, r_m_id=m_id, r_m_type=m_type, source=source)

        MemberRelation.objects.filter(query).filter(relation__in=relations).update(is_deleted=True)

    @classmethod
    def delete_relation(cls, m_id, m_type, r_m_id, r_m_type, relation, user, source):
        m_id = user.id if m_type == "USER" and m_id == -1 else m_id
        try:
            member_object = MemberRelation.objects.get(source=source, m_id=m_id, m_type=m_type, r_m_id=r_m_id,
                                                       r_m_type=r_m_type, relation=relation)
            member_object.is_deleted = True
            member_object.save()
        except:
            print "No such relation exist"

        if relation in SYMMETRIC_RELATIONS:
            try:
                member_object = MemberRelation.objects.get(source=source, m_id=r_m_id, m_type=r_m_type, r_m_id=m_id,
                                                           r_m_type=m_type, relation=relation)
                member_object.is_deleted = True
                member_object.save()
            except:
                print "No such reverse relation exist"

        member_relations = list(
            MemberRelation.objects.filter(
                m_id=m_id, m_type=m_type, r_m_id=r_m_id, r_m_type=r_m_type, source=source).values('relation', 'status'))
        member_relations_info = list()
        for member_relation in member_relations:
            member_relations_info.append({'relation': str(member_relation["relation"]),
                                          'status': str(member_relation["status"])})
        return member_relations_info

    @classmethod
    def get_relations(cls, relation_types, m_id, m_type, r_m_types, source):
        member_relations = MemberRelation.objects.filter(m_id=m_id, m_type=m_type, source=source) \
            .values('r_m_id', 'r_m_type', 'relation', 'status')
        if relation_types:
            member_relations = cls.apply_action_filter(query_objects=member_relations, filter_type="relation",
                                                       filter_value=relation_types, add_additional_filter="__in")
        if r_m_types:
            member_relations = cls.apply_action_filter(query_objects=member_relations, filter_type="r_m_type",
                                                       filter_value=r_m_types, add_additional_filter="__in")
        member_response_dict = MemberRelation.get_member_relation_dict(member_relations)
        return member_response_dict

    @classmethod
    def get_inverse_relations(cls, relation_types, r_m_id, r_m_type, m_types, status, source):
        member_relations = MemberRelation.objects.filter(r_m_id=r_m_id, r_m_type=r_m_type, status=status, source=source)
        if relation_types:
            member_relations = member_relations.filter(relation__in=relation_types)
        if m_types:
            member_relations = member_relations.filter(m_type__in=m_types)
        member_relations = list(member_relations.values('m_id', 'm_type', 'relation'))
        return member_relations

    @staticmethod
    def get_member_relation_dict(member_relations):
        member_relations_dicts_list = list()
        for member in member_relations:
            member_relation_dict = {
                "r_m_id": member["r_m_id"],
                "r_m_type": member["r_m_type"],
                'relation': member["relation"],
                'status': member['status']
            }
            member_relations_dicts_list.append(member_relation_dict)
        return member_relations_dicts_list

    @classmethod
    def apply_action_filter(cls, query_objects, filter_type, filter_value, add_additional_filter=None):
        filtered_objects = list()
        if not add_additional_filter:
            for each_query_object in query_objects:
                if each_query_object[filter_type] == filter_value:
                    filtered_objects.append(each_query_object)
        else:
            if add_additional_filter == "__in":
                for each_query_object in query_objects:
                    if each_query_object[filter_type] in filter_value:
                        filtered_objects.append(each_query_object)
        return filtered_objects

    @staticmethod
    def verify_relations(request_object, source):
        response_objects = list()
        from django.db.models import Q
        query = Q()
        for each_req in request_object:
            query |= Q(m_id=each_req['m_id'], m_type=each_req['m_type'], r_m_id=each_req['r_m_id'],
                       r_m_type=each_req['r_m_type'], relation=each_req['relation'], source=source)
        member_relation_dict_objects_list = MemberRelation.objects.filter(query).values()

        for each_relation_object in request_object:
            unique_key = each_relation_object["unique_key"]
            response_object = MemberRelation.check_relation(each_relation_object, member_relation_dict_objects_list)
            response_object["unique_key"] = unique_key
            response_objects.append(response_object)
        return response_objects

    @classmethod
    def check_relation(cls, relation_object, member_relation_dict_objects_list):
        for each_member_relation_dict_object in member_relation_dict_objects_list:
            if cls.get_member_relation_verify_condition(relation_object, each_member_relation_dict_object):
                return {'is_related': True, 'status': each_member_relation_dict_object['status']}
        return {'is_related': False, 'status': ''}

    @classmethod
    def get_member_relation_verify_condition(cls, relation_object, member_relation_dict_object):
        return member_relation_dict_object["m_id"] == relation_object['m_id'] and \
               member_relation_dict_object["m_type"] == relation_object['m_type'] and \
               member_relation_dict_object["r_m_id"] == relation_object['r_m_id'] and \
               member_relation_dict_object["r_m_type"] == relation_object['r_m_type'] and \
               member_relation_dict_object["relation"] == relation_object['relation']

    @classmethod
    def link_social_user_with_ib_user(cls, user=None, access_token=None, social_token=None,
                                      social_access_token_secret=None, social_provider=None, source='', **kwargs):

        from ib_social.adapters.service_adapter import ServiceAdapter
        service = ServiceAdapter(user=user, access_token=access_token)
        user_social_link = service.ib_users.user_details.link_user_social_account(
            social_provider=social_provider, social_token=social_token,
            social_access_token_secret=social_access_token_secret, source=source)

        user_social_link['social_token'] = social_token
        user_social_link['extra_info'] = social_access_token_secret
        if social_provider == 'facebook':
            cls.get_social_relation_from_facebook(user=user, access_token=access_token,
                                                  user_social_details=user_social_link, source=source)

        elif social_provider == 'twitter':
            cls.get_social_relation_from_twitter(user=user, access_token=access_token,
                                                 user_social_details=user_social_link, source=source)

        return user_social_link

    @classmethod
    def get_social_relation_from_facebook(cls, user, access_token, source, social_provider='facebook',
                                          user_social_details=None):
        from ib_social.adapters.service_adapter import ServiceAdapter
        service = ServiceAdapter(user=user, access_token=access_token)

        if not user_social_details:
            raise NotFound('Social detail for current user not found.', res_status='failed')

        m_user_social_id = user_social_details['social_id']
        social_ids = get_friends_id_from_facebook(user_social_details['social_token'])
        ib_user_details = service.ib_users.user_details.get_usp_by_social_ids(social_ids, social_provider)

        relations = []
        for user_detail in ib_user_details:
            relations.append(
                cls(m_id=user.id, r_m_id=user_detail['user_id'], r_m_type=Variables.USER.value,
                    m_type=Variables.USER.value, relation=Relations.FB_FRIEND.value, source=source,
                    status=RelationshipStatus.ACCEPT.value, m_social_id=m_user_social_id))

            relations.append(
                cls(m_id=user_detail['user_id'], r_m_id=user.id, r_m_type=Variables.USER.value,
                    m_type=Variables.USER.value, relation=Relations.FB_FRIEND.value, source=source,
                    status=RelationshipStatus.ACCEPT.value, m_social_id=m_user_social_id))

        cls.objects.bulk_create(relations)
        return

    @classmethod
    def get_social_relation_from_twitter(cls, user, access_token, source, social_provider='twitter',
                                         user_social_details=None):
        from ib_social.adapters.service_adapter import ServiceAdapter
        service = ServiceAdapter(user=user, access_token=access_token)

        if not user_social_details:
            raise NotFound('Social detail for current user not found.', res_status='failed')

        m_user_social_id = user_social_details['social_id']

        social_ids = get_followers_ids_from_twitter(user_social_details['social_token'],
                                                    user_social_details['extra_info'])
        ib_user_details = service.ib_users.user_details.get_usp_by_social_ids(social_ids, social_provider)

        relations = []
        for user_detail in ib_user_details:
            relations.append(
                cls(m_id=user.id, r_m_id=user_detail['user_id'], r_m_type=Variables.USER.value,
                    m_type=Variables.USER.value, m_social_id=m_user_social_id, source=source,
                    relation=Relations.FOLLOWER.value, status=RelationshipStatus.ACCEPT.value))
        cls.objects.bulk_create(relations)

        return

    @classmethod
    def get_relation_stats(cls, request_data, source):

        ids_list, types_list, relations_list = [], [], []

        for each_data in request_data:
            if each_data["m_id"] not in ids_list:
                ids_list.append(each_data["m_id"])
            if each_data["m_type"] not in types_list:
                types_list.append(each_data["m_type"])
            for each_relation in each_data["relation_types"]:
                if each_relation not in relations_list:
                    relations_list.append(each_relation)

        from django.db.models import Count
        user_relations = list(
            MemberRelation.objects.filter(
                source=source,
                m_id__in=ids_list,
                m_type__in=types_list,
                relation__in=relations_list)
                .values('m_id', 'm_type', 'relation')
                .annotate(count=Count('relation'))
        )

        related_users = list(
            MemberRelation.objects.filter(
                source=source,
                r_m_id__in=ids_list,
                r_m_type__in=types_list,
                relation__in=relations_list)
                .values('r_m_id', 'r_m_type', 'relation')
                .annotate(count=Count('relation'))
        )

        related_users_dict = dict()
        for each in related_users:
            key = "%d-%s" % (each['r_m_id'], each['r_m_type'])
            _obj = {"relation_val": each['relation'], "relation_count": each["count"]}
            if key not in related_users_dict:
                related_users_dict[key] = [_obj]
            else:
                related_users_dict[key].append(_obj)

        user_relations_dict = dict()
        for each in user_relations:
            key = "%d-%s" % (each['m_id'], each['m_type'])
            _obj = {"relation_val": each['relation'], "relation_count": each["count"]}
            if key not in user_relations_dict:
                user_relations_dict[key] = [_obj]
            else:
                user_relations_dict[key].append(_obj)

        for each_data in request_data:
            key = "%d-%s" % (each_data['m_id'], each_data['m_type'])
            each_data.update({
                'user_relations_count': user_relations_dict.get(key, []),
                'related_users_count': related_users_dict.get(key, []),
            })
        return request_data

    @classmethod
    def delink_user_social_account(cls, user=None, social_provider=None, access_token=None, source=''):

        from ib_social.adapters.service_adapter import ServiceAdapter
        service_adapter = ServiceAdapter(user=user, access_token=access_token)

        social_detail = service_adapter.ib_users.user_details.delink_user_social_account(
            social_provider=social_provider, source=source)

        m_social_id = social_detail['social_id']

        cls.objects.filter(m_social_id=m_social_id, m_id=user.id, source=source).update(is_deleted=True)

        return
