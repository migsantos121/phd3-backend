from datetime import datetime
from django.db import models

from ib_articles.models.keyword_group import KeywordGroup
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel
from ib_common.vernacular_utils.vernacular_utilities_class import VernacularUtilitiesClass


class Keyword(AbstractDateTimeModel, VernacularUtilitiesClass):
    _keyword = models.CharField(max_length=300)
    keyword_group = models.ForeignKey(KeywordGroup)
    unique_datetime = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self._keyword)

    class Meta:
        unique_together = ('keyword_group', '_keyword')

    @property
    def keyword(self):
        return self._i_keyword

    @classmethod
    def add_keywords(cls, user, keywords_request_data):
        group_ids = list(set([each_keyword_data["group_id"] for each_keyword_data in keywords_request_data]))
        default_group = None
        if -1 in group_ids:
            group_ids.remove(-1)
            default_group = cls.get_default_group()
            group_ids.append(default_group.id)
        if default_group:
            for each_keyword_data in keywords_request_data:
                if each_keyword_data['group_id'] == -1:
                    each_keyword_data['group_id'] = default_group.id
        group_objects = cls.get_group_objects(group_ids)
        existing_v_keywords_objects = cls.get_existing_v_keywords_objects(keywords_request_data=keywords_request_data,
                                                                          user=user)
        present_time = datetime.now()
        unsaved_keyword_objects = []
        for each_keyword_data in keywords_request_data:
            keyword = each_keyword_data["keyword"]
            keyword_group = cls.get_keyword_group(group_id=each_keyword_data["group_id"], group_objects=group_objects)
            is_keyword_data_object_exist = cls.check_is_keyword_data_object_exist(keyword=keyword,
                                                                                  keyword_group=keyword_group,
                                                                                  existing_v_keywords_objects=existing_v_keywords_objects)
            if not is_keyword_data_object_exist:
                keyword_object = Keyword(_keyword=keyword, keyword_group=keyword_group, unique_datetime=present_time)
                unsaved_keyword_objects.append(keyword_object)
        Keyword.objects.bulk_create(unsaved_keyword_objects)
        created_keyword_objects = Keyword.objects.filter(unique_datetime=present_time)
        cls.create_v_keyword_objects(keyword_objects=created_keyword_objects, user=user)
        keywords_response_dicts = cls.get_keywords_response_dicts(created_keyword_objects=created_keyword_objects,
                                                                  existing_v_keywords_objects=existing_v_keywords_objects)
        return keywords_response_dicts

    @classmethod
    def get_keywords_response_dicts(cls, created_keyword_objects, existing_v_keywords_objects):
        keywords_response_dicts = []
        for each_v_keywords_obj in existing_v_keywords_objects:
            keyword_response_dict = {
                "keyword": each_v_keywords_obj.v_keyword,
                "keyword_id": each_v_keywords_obj.id
            }
            keywords_response_dicts.append(keyword_response_dict)

        for each_keyword_object in created_keyword_objects:
            keyword_response_dict = {
                "keyword": each_keyword_object.keyword,
                "keyword_id": each_keyword_object.id
            }
            keywords_response_dicts.append(keyword_response_dict)
        return keywords_response_dicts

    @classmethod
    def create_v_keyword_objects(cls, keyword_objects, user):
        from ib_articles.models import KeywordVernacularDetails
        unsaved_v_keyword_objects = []
        for each_keyword_object in keyword_objects:
            keyword_v_object = KeywordVernacularDetails(v_keyword=each_keyword_object.keyword,
                                                        keyword=each_keyword_object, language_name=user.language)
            unsaved_v_keyword_objects.append(keyword_v_object)
        KeywordVernacularDetails.objects.bulk_create(unsaved_v_keyword_objects)
        return

    @classmethod
    def get_group_objects(cls, group_ids):
        group_objects = list(KeywordGroup.objects.filter(id__in=group_ids))
        if len(group_ids) != len(group_objects):
            from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed
            raise ExpectationFailed({}, res_status="One of keyword group not exist")
        return group_objects

    @classmethod
    def get_default_group(cls):
        from django.conf import settings
        default_group, is_created = KeywordGroup.objects.get_or_create(group=settings.DEFAULT_GROUP,
                                                                       group_weight=settings.DEFAULT_GROUP_WEIGHT)
        return default_group

    @classmethod
    def get_keyword_group(cls, group_id, group_objects):
        for each_group_object in group_objects:
            if each_group_object.id == group_id:
                return each_group_object

    @classmethod
    def check_is_keyword_data_object_exist(cls, existing_v_keywords_objects, keyword, keyword_group):
        for each_v_keywords_obj in existing_v_keywords_objects:
            if each_v_keywords_obj.v_keyword == keyword and each_v_keywords_obj.keyword.keyword_group == keyword_group:
                return True
        return False

    @classmethod
    def get_existing_v_keywords_objects(cls, keywords_request_data, user):
        from django.db.models import Q
        query = Q()
        for each_keyword_data in keywords_request_data:
            query |= Q(v_keyword=each_keyword_data["keyword"], language_name=user.language,
                       keyword__keyword_group__id=each_keyword_data["group_id"])
        from ib_articles.models import KeywordVernacularDetails
        keyword_objs = list(KeywordVernacularDetails.objects.filter(query).select_related("keyword"))
        return keyword_objs

    @classmethod
    def get_keywords(cls, user, keyword_ids=None, search_q=None, limit=None, offset=None):

        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]

        if keyword_ids is None:
            keyword_ids = []

        _objects = cls.objects.filter()

        if keyword_ids:
            _objects = _objects.filter(id__in=keyword_ids)

        if search_q:
            _objects = _objects.filter(_keyword__icontains=search_q)
        # _objects = _objects.prefetch_related('vernacular_details')

        if limit:
            _objects = _objects[offset:offset+limit]

        keywords_list = []
        [each.set_language_specific_attributes(language_name=language_name) for each in _objects]

        for each in _objects:
            _dict = {
                "keyword": each.keyword,
                "keyword_id": each.id
            }
            keywords_list.append(_dict)
        return keywords_list
