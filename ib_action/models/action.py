from django.db import models
from django.db.models import Q, Count
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel


class Action(AbstractDateTimeModel):
    ACTION_CHOICES = (
        ('RATE', 'RATE'),
        ('LIKE', 'LIKE'),
        ('VOTE', 'VOTE'),
        ('LOVE', 'LOVE'),
        ('SHARE', 'SHARE'),
        ('FOLLOW', 'FOLLOW'),
        ('BOOKMARK', 'BOOKMARK'),
        ('BOOK_STATUS', 'BOOK_STATUS'),
        ('BOOK_PROGRESS', 'BOOK_PROGRESS'),
        ('FAVOURITE', 'FAVOURITE'),
        ('SUBSCRIBE', 'SUBSCRIBE'),
        ('REPORT', 'REPORT'),
        ('HELPFUL', 'HELPFUL'),
        ('ATTEND', 'ATTEND'),
        ('SAVE_STATUS', 'SAVE_STATUS'),
    )  # we have to add action choice in specfile also to accept request

    entity_id = models.IntegerField()
    entity_type = models.CharField(max_length=100)
    user_id = models.IntegerField()
    source = models.CharField(max_length=100)
    action_type = models.CharField(max_length=30, choices=ACTION_CHOICES)
    action_value = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return unicode("%d-%s-%s" % (self.id, self.source, self.action_type))

    @classmethod
    def get_friends_actions(cls, source, entity_id, entity_type, action_type, user_id, user_type, user, limit, offset,
                            access_token):
        user_id = user.id if (user_id == -1 and user_type == "USER") else user_id
        from ib_action.adapters.get_friends_list_adapter import get_friends_list_adapter
        friends_info_list = get_friends_list_adapter(user_id=user_id, user_type="USER", limit=0, offset=0,
                                                     user=user, access_token=access_token)
        friends_list = friends_info_list["friends"]
        print friends_list
        friends_user_ids = [each_friend["user_id"] for each_friend in friends_list]
        friends_action_objects = list(Action.objects.filter(entity_type=entity_type, action_type=action_type,
                                                            source=source, entity_id=entity_id,
                                                            user_id__in=friends_user_ids))
        count = len(friends_action_objects)
        friends_actions_response = []
        for each_friend_action in friends_action_objects:
            friend_detials_dict = cls.get_friend_info(user_id=each_friend_action.user_id, friends_list=friends_list)
            friend_detials_dict["action_value"] = each_friend_action.action_value
            friends_actions_response.append(friend_detials_dict)
        response_object = {"count": count, "friends_actions": friends_actions_response}
        return response_object

    @classmethod
    def get_friend_info(cls, user_id, friends_list):
        for each_friend_info in friends_list:
            if each_friend_info["user_id"] == user_id:
                return each_friend_info

    @staticmethod
    def get_saved_items(source, user, action_type, filter_entity_types, offset, limit):
        action_objects = list(Action.objects.filter(source=source, action_type=action_type, user_id=user.id).
                              exclude(action_value="NEUTRAL").order_by('-creation_datetime'))

        if not filter_entity_types:
            if limit > 0:
                action_objects = action_objects[offset:offset + limit]
            saved_item_dicts = Action.get_saved_item_dicts(action_objects=action_objects)
            return saved_item_dicts

        filtered_action_objects = Action.apply_entity_type_filter(action_objects=action_objects,
                                                                  filter_entity_types=filter_entity_types)
        saved_item_dicts = Action.get_saved_item_dicts(action_objects=filtered_action_objects)
        return saved_item_dicts

    @classmethod
    def apply_entity_type_filter(cls, action_objects, filter_entity_types):
        filtered_action_objects = list()
        for each_entity_type_filter in filter_entity_types:
            entity_type_action_objects = list()
            entity_type = each_entity_type_filter["entity_type"]
            offset = each_entity_type_filter.get("offset", 0)
            limit = each_entity_type_filter.get("limit", 0)
            for each_action_object in action_objects:
                if each_action_object.entity_type == entity_type:
                    entity_type_action_objects.append(each_action_object)
            if limit > 0:
                entity_type_action_objects = entity_type_action_objects[offset:offset + limit]
            filtered_action_objects.extend(entity_type_action_objects)
        return filtered_action_objects

    @classmethod
    def get_saved_item_dicts(cls, action_objects):
        saved_item_dicts = []
        for each_action_object in action_objects:
            saved_item_dict = {
                "entity_id": each_action_object.entity_id,
                "entity_type": each_action_object.entity_type,
                "user_id": each_action_object.user_id,
                "action_type": each_action_object.action_type,
                "action_value": each_action_object.action_value
            }
            saved_item_dicts.append(saved_item_dict)
        return saved_item_dicts

    @staticmethod
    def add_action_record(action_value, source, entity_id, action_type, entity_type, user_id):

        if action_type == "BOOK_PROGRESS" or action_type == "RATE":
            try:
                print int(action_value)
            except:
                from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed
                raise ExpectationFailed({}, res_status="Action value is not an integer")

        action, is_created = Action.objects.get_or_create(source=source,
                                                          action_type=action_type,
                                                          entity_id=entity_id,
                                                          entity_type=entity_type,
                                                          user_id=user_id
                                                          )
        if action_type == "SHARE":
            if is_created:
                action.action_value = str(1)
            else:
                action.action_value = str(int(action.action_value) + 1)
        else:
            action.action_value = action_value
        action.save()
        print action
        response = Action.get_actions_summary(entity_id=entity_id, source=source, user_id=user_id,
                                              entity_type=entity_type)

        callback_dict = {'action_id': action.id, 'action_type': action.action_type, 'entity_id': action.entity_id,
                         'entity_type': action.entity_type, 'action_value': action.action_value,
                         'user_id': action.user_id, 'is_created': is_created}
        return response, callback_dict

    @staticmethod
    def get_actions_summary(entity_id, entity_type, source, user_id, action_type_filters=None):
        actions = Action.objects.filter(entity_id=entity_id, entity_type=entity_type, source=source) \
            .values("action_value", "source", "entity_id", "action_type", "entity_type", "user_id")
        if action_type_filters:
            actions = actions.filter(action_type__in=action_type_filters)
        else:
            action_type_filters = []
            for each_choice in Action.ACTION_CHOICES:
                action_type_filters.append(each_choice[0])
        actions = list(actions)
        response_object = Action.calculate_summary_reports(actions, user_id, action_type_filters)
        return response_object

    @staticmethod
    def get_selected_users_actions_summary(entities, source, user_ids, action_type_filters):
        entity_queries = [Q(entity_id=each_entity['entity_id'], entity_type=each_entity['entity_type']) for each_entity
                          in entities]
        if not entity_queries:
            return list()
        query = entity_queries.pop()
        for item in entity_queries:
            query |= item
        actions = Action.objects.filter(source=source).filter(query) \
            .values("action_value", "source", "entity_id", "action_type", "entity_type", "user_id")
        actions = list(actions)
        if action_type_filters:
            actions = Action.apply_action_filter(actions, filter_type="action_type", filter_value=action_type_filters,
                                                 add_additional_filter="__in")
        else:
            action_type_filters = []
            for each_choice in Action.ACTION_CHOICES:
                action_type_filters.append(each_choice[0])

        # Todo need to consider the case when user_ids is empty
        entities_action_summaries = []
        for each_entity in entities:
            entity_info_dict = Action.get_entity_info_dict(entity=each_entity, actions=actions, user_ids=user_ids,
                                                           action_type_filters=action_type_filters)
            entities_action_summaries.append(entity_info_dict)
        return entities_action_summaries

    @staticmethod
    def get_entities_with_summaries(source, user_ids, entity_type):

        actions = Action.objects.filter(source=source, entity_type=entity_type) \
            .values("action_value", "source", "entity_id", "action_type", "entity_type", "user_id")
        actions = list(actions)
        action_type_filters = [each_choice[0] for each_choice in Action.ACTION_CHOICES]
        entity_ids = Action.objects.filter(user_id__in=user_ids).values_list("entity_id", flat=True).distinct()

        entities_action_summaries = []
        for each_entity_id in entity_ids:
            is_all_users_in_entity = Action.check_all_users_in_entity(user_ids, each_entity_id, actions)
            if is_all_users_in_entity:
                entity_dict = {
                    "entity_id": each_entity_id,
                    "entity_type": entity_type
                }
                entity_info_dict = Action.get_entity_info_dict(entity=entity_dict, actions=actions, user_ids=user_ids,
                                                               action_type_filters=action_type_filters)
                entities_action_summaries.append(entity_info_dict)
        return entities_action_summaries

    @classmethod
    def check_all_users_in_entity(cls, user_ids, entity_id, actions):
        entity_users_list = cls.get_entity_users_list(entity_id, actions)
        for each_user_id in user_ids:
            if each_user_id not in entity_users_list:
                return False
        return True

    @classmethod
    def get_entity_users_list(cls, entity_id, actions):
        entity_actions_list = cls.apply_action_filter(actions, filter_type="entity_id", filter_value=entity_id)
        user_ids = [each_entity_action["user_id"] for each_entity_action in entity_actions_list]
        return user_ids

    @classmethod
    def get_entity_info_dict(cls, entity, actions, user_ids, action_type_filters):
        entity_id = entity["entity_id"]
        entity_type = entity["entity_type"]
        entity_id_specific_actions = cls.apply_action_filter(actions, filter_type="entity_id", filter_value=entity_id)
        entity_type_specific_actions = cls.apply_action_filter(entity_id_specific_actions, filter_type="entity_type",
                                                               filter_value=entity_type)
        entity_summary_dict = Action.calculate_summary_reports(actions=entity_type_specific_actions, user_id=None,
                                                               action_type_filters=action_type_filters)
        users_actions_summaries = cls.get_users_actions_summaries(user_ids=user_ids,
                                                                  actions=entity_type_specific_actions,
                                                                  action_type_filters=action_type_filters)
        entity_summary_dict["users_actions_summaries"] = users_actions_summaries
        entity_summary_dict["entity_id"] = entity_id
        entity_summary_dict["entity_type"] = entity_type
        return entity_summary_dict

    @classmethod
    def get_users_actions_summaries(cls, user_ids, actions, action_type_filters):
        if not user_ids:
            user_ids = [action['user_id'] for action in actions]
        users_actions_summaries = []
        for each_user_id in user_ids:
            user_actions = cls.apply_action_filter(actions, filter_type="user_id", filter_value=each_user_id)
            user_actions_summary = cls.get_user_actions_summary(user_actions, action_type_filters)
            user_actions_summary_object = {
                "user_id": each_user_id,
                "user_actions": user_actions_summary
            }
            users_actions_summaries.append(user_actions_summary_object)
        return users_actions_summaries

    @classmethod
    def calculate_summary_reports(cls, actions, user_id, action_type_filters):
        response_object = dict()
        if "LIKE" in action_type_filters:
            like_actions = cls.apply_action_filter(actions, filter_type="action_type", filter_value="LIKE")
            like_actions_summary = cls.get_like_actions_summary(like_actions)
            response_object["like_summary"] = like_actions_summary
        if "BOOK_STATUS" in action_type_filters:
            book_status_actions = cls.apply_action_filter(actions, filter_type="action_type",
                                                          filter_value="BOOK_STATUS")
            book_status_actions_summary = cls.get_book_status_actions_summary(book_status_actions)
            response_object["book_status_summary"] = book_status_actions_summary
        if "SAVE_STATUS" in action_type_filters:
            save_status_actions = cls.apply_action_filter(actions, filter_type="action_type",
                                                          filter_value="SAVE_STATUS")
            save_status_actions_summary = cls.get_save_status_actions_summary(save_status_actions)
            response_object["save_status_summary"] = save_status_actions_summary
        if "SUBSCRIBE" in action_type_filters:
            subscribe_actions = cls.apply_action_filter(actions, filter_type="action_type", filter_value="SUBSCRIBE")
            subscribe_actions_summary = cls.get_subscribe_actions_summary(subscribe_actions)
            response_object["subscribe_summary"] = subscribe_actions_summary
        if "ATTEND" in action_type_filters:
            attend_actions = cls.apply_action_filter(actions, filter_type="action_type", filter_value="ATTEND")
            attend_actions_summary = cls.get_attend_actions_summary(attend_actions)
            response_object["attend_summary"] = attend_actions_summary
        if "RATE" in action_type_filters:
            rate_actions = cls.apply_action_filter(actions, filter_type="action_type", filter_value="RATE")
            rate_actions_summary = cls.get_rate_actions_summary(rate_actions)
            response_object["rating_summary"] = rate_actions_summary
        if "VOTE" in action_type_filters:
            vote_actions = cls.apply_action_filter(actions, filter_type="action_type", filter_value="VOTE")
            vote_actions_summary = cls.get_vote_actions_summary(vote_actions)
            response_object["vote_summary"] = vote_actions_summary
        if "FAVOURITE" in action_type_filters:
            favourite_actions = cls.apply_action_filter(actions, filter_type="action_type", filter_value="FAVOURITE")
            favourite_actions_summary = cls.get_favourite_actions_summary(favourite_actions)
            response_object["favourite_summary"] = favourite_actions_summary
        if "LOVE" in action_type_filters:
            love_actions = cls.apply_action_filter(actions, filter_type="action_type", filter_value="LOVE")
            love_actions_summary = cls.get_love_actions_summary(love_actions)
            response_object["love_summary"] = love_actions_summary
        if "SHARE" in action_type_filters:
            share_actions = cls.apply_action_filter(actions, filter_type="action_type", filter_value="SHARE")
            share_actions_summary = cls.get_share_actions_summary(share_actions)
            response_object["share_summary"] = share_actions_summary
        if "FOLLOW" in action_type_filters:
            follow_actions = cls.apply_action_filter(actions, filter_type="action_type", filter_value="FOLLOW")
            follow_actions_summary = cls.get_follow_actions_summary(follow_actions)
            response_object["follow_summary"] = follow_actions_summary
        if "BOOKMARK" in action_type_filters:
            bookmark_actions = cls.apply_action_filter(actions, filter_type="action_type", filter_value="BOOKMARK")
            bookmark_actions_summary = cls.get_bookmark_actions_summary(bookmark_actions)
            response_object["bookmark_summary"] = bookmark_actions_summary
        if "REPORT" in action_type_filters:
            report_actions = cls.apply_action_filter(actions, filter_type="action_type", filter_value="REPORT")
            report_actions_summary = cls.get_report_actions_summary(report_actions)
            response_object["report_summary"] = report_actions_summary
        if "HELPFUL" in action_type_filters:
            helpful_actions = cls.apply_action_filter(actions, filter_type="action_type", filter_value="HELPFUL")
            helpful_actions_summary = cls.get_helpful_actions_summary(helpful_actions)
            response_object["helpful_summary"] = helpful_actions_summary
        if user_id:
            user_actions = cls.apply_action_filter(actions, filter_type="user_id", filter_value=user_id)
            user_actions_summary = cls.get_user_actions_summary(user_actions, action_type_filters)
            response_object["user_actions"] = user_actions_summary
        return response_object

    @classmethod
    def get_like_actions_summary(cls, like_actions):
        positive_objects = cls.apply_action_filter(action_objects=like_actions, filter_type="action_value",
                                                   filter_value="LIKE")
        negative_objects = cls.apply_action_filter(action_objects=like_actions, filter_type="action_value",
                                                   filter_value="DISLIKE")
        response = {
            "positive": len(positive_objects),
            "negative": len(negative_objects)
        }
        return response

    @classmethod
    def get_book_status_actions_summary(cls, book_status_actions):
        read_objects = cls.apply_action_filter(action_objects=book_status_actions, filter_type="action_value",
                                               filter_value="READ")
        want_to_read_objects = cls.apply_action_filter(action_objects=book_status_actions, filter_type="action_value",
                                                       filter_value="WANT_TO_READ")
        stared_reading_objects = cls.apply_action_filter(action_objects=book_status_actions, filter_type="action_value",
                                                         filter_value="STARTED_READING")
        response = {
            "read": len(read_objects),
            "want_to_read": len(want_to_read_objects),
            "started_reading": len(stared_reading_objects)
        }
        return response

    @classmethod
    def get_save_status_actions_summary(cls, save_status_actions):
        read_objects = cls.apply_action_filter(action_objects=save_status_actions, filter_type="action_value",
                                               filter_value="SAVED")
        want_to_read_objects = cls.apply_action_filter(action_objects=save_status_actions, filter_type="action_value",
                                                       filter_value="COMPLETED")
        response = {
            "saved": len(read_objects),
            "completed": len(want_to_read_objects)
        }
        return response

    @classmethod
    def get_vote_actions_summary(cls, vote_actions):
        positive_objects = cls.apply_action_filter(action_objects=vote_actions, filter_type="action_value",
                                                   filter_value="UPVOTE")
        negative_objects = cls.apply_action_filter(action_objects=vote_actions, filter_type="action_value",
                                                   filter_value="DOWNVOTE")
        response = {
            "positive": len(positive_objects),
            "negative": len(negative_objects)
        }
        return response

    @classmethod
    def get_favourite_actions_summary(cls, favourite_actions):
        positive_objects = cls.apply_action_filter(action_objects=favourite_actions, filter_type="action_value",
                                                   filter_value="FAVOURITE")
        response = {
            "positive": len(positive_objects)
        }
        return response

    @classmethod
    def get_subscribe_actions_summary(cls, subscribe_actions):
        positive_objects = cls.apply_action_filter(action_objects=subscribe_actions, filter_type="action_value",
                                                   filter_value="SUBSCRIBE")
        response = {
            "positive": len(positive_objects)
        }
        return response

    @classmethod
    def get_attend_actions_summary(cls, attend_actions):
        positive_objects = cls.apply_action_filter(action_objects=attend_actions, filter_type="action_value",
                                                   filter_value="ATTEND")
        response = {
            "positive": len(positive_objects)
        }
        return response

    @classmethod
    def get_share_actions_summary(cls, share_actions):
        total_shares = 0
        for each_positive_object in share_actions:
            try:
                total_shares = total_shares + int(each_positive_object["action_value"])
            except:
                print "Something went wrong with share action value"
        response = {
            "positive": total_shares
        }
        return response

    @classmethod
    def get_follow_actions_summary(cls, share_actions):
        positive_objects = cls.apply_action_filter(action_objects=share_actions, filter_type="action_value",
                                                   filter_value="FOLLOW")
        response = {
            "positive": len(positive_objects)
        }
        return response

    @classmethod
    def get_love_actions_summary(cls, love_actions):
        positive_objects = cls.apply_action_filter(action_objects=love_actions, filter_type="action_value",
                                                   filter_value="LOVE")
        response = {
            "positive": len(positive_objects)
        }
        return response

    @classmethod
    def get_bookmark_actions_summary(cls, bookmark_actions):
        positive_objects = cls.apply_action_filter(action_objects=bookmark_actions, filter_type="action_value",
                                                   filter_value="BOOKMARK")
        response = {
            "positive": len(positive_objects)
        }
        return response

    @classmethod
    def get_report_actions_summary(cls, report_actions):
        positive_objects = cls.apply_action_filter(action_objects=report_actions, filter_type="action_value",
                                                   filter_value="REPORT")
        response = {
            "positive": len(positive_objects)
        }
        return response

    @classmethod
    def get_helpful_actions_summary(cls, helpful_actions):
        positive_objects = cls.apply_action_filter(action_objects=helpful_actions, filter_type="action_value",
                                                   filter_value="HELPFUL")
        response = {
            "positive": len(positive_objects)
        }
        return response

    @classmethod
    def get_rate_actions_summary(cls, rate_actions):
        rate_actions_counts = []
        for each_rate_action in rate_actions:
            rate_actions_counts.append(each_rate_action["action_value"])
        rate_action_objects = []
        for each_rate_value in range(0, 11):
            rate_object = {
                "r_count": rate_actions_counts.count(str(each_rate_value)),
                "r_value": each_rate_value
            }
            rate_action_objects.append(rate_object)
        return rate_action_objects

    @classmethod
    def get_user_actions_summary(cls, user_actions, action_type_filters):
        user_action_objects = []
        for each_choice in action_type_filters:
            filter_value = each_choice
            record = cls.apply_action_filter(user_actions, filter_type="action_type", filter_value=filter_value)
            if record:
                action_value = record[0]["action_value"]
            else:
                action_value = "NEUTRAL"
            action = {
                "action_type": filter_value,
                "action_value": action_value
            }
            user_action_objects.append(action)
        return user_action_objects

    @classmethod
    def apply_action_filter(cls, action_objects, filter_type, filter_value, add_additional_filter=None):
        filtered_objects = []
        if not add_additional_filter:
            for each_action in action_objects:
                if each_action[filter_type] == filter_value:
                    filtered_objects.append(each_action)
        else:
            if add_additional_filter == "__in":
                for each_action in action_objects:
                    if each_action[filter_type] in filter_value:
                        filtered_objects.append(each_action)
        return filtered_objects

    class Meta:
        unique_together = ("entity_id", "entity_type", 'user_id', 'source', 'action_type')

    @classmethod
    def get_entities_with_user_action(cls, **kwargs):

        source = kwargs["source"]
        offset = kwargs["offset"]
        limit = kwargs["limit"]
        action_type = kwargs["action_type"]
        entity_type = kwargs["entity_type"]

        user_id = kwargs["user_id"]
        actions = cls.objects.filter(source=source, user_id=user_id, action_type=action_type,
                                     entity_type=entity_type).values()
        total = len(actions)
        actions_list = actions[offset: offset + limit]
        response = {
            "total": total,
            "actions": actions_list
        }
        return response

    @classmethod
    def get_entities_with_user_actions(cls, **kwargs):

        source = kwargs["source"]
        offset = kwargs["offset"]
        limit = kwargs["limit"]
        action_types = kwargs["action_types"]
        action_values = kwargs["action_values"]
        entity_types = kwargs["entity_types"]
        user_id = kwargs["user_id"]

        actions = cls.objects.filter(source=source, user_id=user_id, action_type__in=action_types,
                                     entity_type__in=entity_types)
        if action_values:
            actions = actions.filter(action_value__in=action_values)
        if limit != 0:
            actions = actions[offset: offset + limit]
        return actions.values()

    @classmethod
    def get_user_counts(cls, **kwargs):

        request_data = kwargs["request_data"]
        user = kwargs["user"]

        source = request_data["source"]
        entity_types = request_data["entity_types"]
        action_types = request_data["action_types"]
        action_values = request_data["action_values"]

        actions = cls.objects.filter(source=source, user_id=user.id, action_type__in=action_types,
                                     entity_type__in=entity_types)
        if action_values:
            actions = actions.filter(action_value__in=action_values)

        actions = actions.values('entity_id', 'entity_type', 'action_type', 'action_value').annotate(
            entity_count=Count('entity_type'))
        return actions
