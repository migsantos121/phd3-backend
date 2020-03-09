from django.db import models
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel

from .category import Category


class UserCategoryMap(AbstractDateTimeModel):
    category = models.ForeignKey(Category)
    user_id = models.IntegerField()
    is_blocked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user_id', 'category')

    def __unicode__(self):
        return unicode(self.category)

    @classmethod
    def add_user_categories(cls, user, category_ids):
        _objects = []
        user_id = user.id
        for each_id in category_ids:
            _obj = cls(user_id=user_id, category_id=each_id)
            _objects.append(_obj)
        cls.objects.bulk_create(_objects)

    @classmethod
    def add_user_category(cls, user, category_id):
        user_id = user.id
        cls.objects.get_or_create(user_id=user_id, category_id=category_id)

    @classmethod
    def remove_user_categories(cls, user, category_ids):
        cls.objects.filter(user_id=user.id, category_id__in=category_ids).delete()

    @classmethod
    def get_user_categories(cls, user, _adapter, category_ids=None):
        from ib_common.vernacular_utils.vernacular_utilities_class import VernacularUtilitiesClass
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]

        user_id = user.id
        _objects = cls.objects.filter(user_id=user_id).select_related('category').prefetch_related(
            'category__vernacular_details')

        if category_ids:
            _objects = _objects.filter(category_id__in=category_ids)

        [each.category.set_language_specific_attributes(language_name=language_name) for each in _objects]

        _ids = []
        response_dict = dict()
        for each in _objects:
            _dict = {
                "category": each.category.category,
                "category_id": each.category_id,
            }
            response_dict[each.id] = _dict
            _ids.append(each.id)

        from ib_recommender.models import UserKeywordMap
        _maps = UserKeywordMap.objects.filter(user_id=user_id)
        # if _ids:
        #     _maps = _maps.filter(user_category_map_id__in=_ids)
        keywords_map = list(_maps.values('keyword_id', 'user_category_map_id'))

        keyword_ids = []
        keywords_map_dict = dict()
        for each in keywords_map:
            if each['keyword_id'] not in keyword_ids:
                keyword_ids.append(each['keyword_id'])
            if each['user_category_map_id'] not in keywords_map_dict:
                keywords_map_dict[each['user_category_map_id']] = [each['keyword_id']]
            else:
                keywords_map_dict[each['user_category_map_id']].append(each['keyword_id'])

        keywords_list = _adapter.ib_articles.get_keywords(keyword_ids)
        keywords_dict = dict()
        for each in keywords_list:
            keywords_dict[each['keyword_id']] = each

        _response_list = []
        for key, val in response_dict.items():

            keywords = keywords_map_dict.get(key, [])
            keywords_list = []
            for each_keyword in keywords:
                keywords_list.append(keywords_dict.get(each_keyword, []))
            val.update({"keywords": keywords_list})
            _response_list.append(val)
        return _response_list
