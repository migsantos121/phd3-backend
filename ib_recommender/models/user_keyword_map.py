from django.db import models

from .user_category_map import UserCategoryMap


class UserKeywordMap(models.Model):
    user_id = models.IntegerField()
    keyword_id = models.IntegerField()
    interest_score = models.FloatField()
    is_blocked = models.BooleanField(default=False)
    user_category_map = models.ForeignKey(UserCategoryMap, null=True, blank=True)

    class Meta:
        unique_together = ('user_id', 'keyword_id')

    def __unicode__(self):
        return unicode("%s %s" % (self.user_id, self.keyword_id))

    @classmethod
    def get_user_category_map(cls, user_id, category_id):
        user_category_map = None
        if category_id is not None:
            try:
                user_category_map = UserCategoryMap.objects.get(user_id=user_id, category_id=category_id)
            except UserCategoryMap.DoesNotExist:
                from django_swagger_utils.drf_server.exceptions.not_found import NotFound
                raise NotFound("CategoryId not found")
        return user_category_map

    @classmethod
    def add_user_keywords(cls, user, keyword_ids, category_id=None):
        user_id = user.id
        user_category_map = cls.get_user_category_map(user_id, category_id)

        existing_ids = list(
            cls.objects.filter(user_id=user_id, keyword_id__in=keyword_ids).values_list('keyword_id', flat=True))
        new_ids = set(keyword_ids) - set(existing_ids)

        _objects = []
        from django.conf import settings
        for each_id in new_ids:
            _object = cls(user_id=user_id, keyword_id=each_id,
                          interest_score=settings.DEFAULT_SOURCE_KEYWORDS_RELEVANCE,
                          user_category_map=user_category_map)
            _objects.append(_object)

        cls.objects.bulk_create(_objects)
        # todo ask about the default user interest score

    @classmethod
    def remove_user_keywords(cls, user, keyword_ids, category_id=None):
        user_category_map = cls.get_user_category_map(user.id, category_id)
        _objects = cls.objects.filter(user_id=user.id, keyword_id__in=keyword_ids)
        if user_category_map:
            _objects = _objects.filter(user_category_map=user_category_map)
        _objects.delete()

    @classmethod
    def block_user_keywords(cls, user, keyword_ids, is_blocked):
        cls.objects.filter(user_id=user.id, keyword_id__in=keyword_ids).update(is_blocked=is_blocked)

    @classmethod
    def get_user_keywords(cls, user_id, is_blocked, _adapter):
        from ib_recommender.models import UserKeywordMap
        keyword_ids = list(
            UserKeywordMap.objects.filter(user_id=user_id, is_blocked=is_blocked).values_list('keyword_id', flat=True))
        return _adapter.ib_articles.get_keywords(keyword_ids)
