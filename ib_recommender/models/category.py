from django.db import models

from ib_common.models.abstract_date_time_model import AbstractDateTimeModel
from ib_common.vernacular_utils.vernacular_utilities_class import VernacularUtilitiesClass


class Category(AbstractDateTimeModel, VernacularUtilitiesClass):
    _category = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return unicode(self._category)

    @property
    def category(self):
        return self._i_category

    @classmethod
    def add_category(cls, user, category):
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]
        from django_swagger_utils.drf_server.exceptions.not_found import NotFound
        try:
            category_obj = cls.get_category_by_name(category=category)
        except NotFound:
            category_obj = cls(_category=category)
            category_obj.save()

            from ib_recommender.models.category_vernacular_details import CategoryVernacularDetails
            CategoryVernacularDetails.objects.create(language_name=language_name,
                                                     category=category_obj,
                                                     v_category=category)

        from ib_recommender.models import UserCategoryMap
        UserCategoryMap.add_user_category(user, category_id=category_obj.id)
        return {'category_id': category_obj.id}

    @classmethod
    def remove_category(cls, user, category_id):
        try:
            category_obj = cls.objects.get(id=category_id)
            from ib_recommender.models import UserCategoryMap
            UserCategoryMap.remove_user_categories(user, category_ids=[category_id])
        except cls.DoesNotExist:
            from django_swagger_utils.drf_server.exceptions.not_found import NotFound
            raise NotFound("Category Id not found")

    @classmethod
    def get_category_by_name(cls, category):
        try:
            category_obj = cls.objects.get(_category=category)
            return category_obj
        except cls.DoesNotExist:
            from django_swagger_utils.drf_server.exceptions.not_found import NotFound
            raise NotFound("Category Id not found")
