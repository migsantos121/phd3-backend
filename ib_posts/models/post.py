from django.db import models
from django.db.models import Count
from django_swagger_utils.drf_server.exceptions.bad_request import BadRequest
from django_swagger_utils.drf_server.exceptions.forbidden import Forbidden
from django_swagger_utils.drf_server.exceptions.not_found import NotFound
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel
from ib_common.vernacular_utils.vernacular_utilities_class import VernacularUtilitiesClass

from ib_posts.constants import variables
from ib_posts.constants.variables import MEDIA_TYPE


class Post(AbstractDateTimeModel, VernacularUtilitiesClass):
    _contents = models.CharField(max_length=1000)
    _multimedia_url = models.CharField(max_length=500, null=True, blank=True)
    _multimedia_type = models.CharField(max_length=200, null=True, blank=True, choices=MEDIA_TYPE)
    user_id = models.IntegerField()
    article_id = models.IntegerField(default=-1)

    class Meta:
        app_label = 'ib_posts'
        ordering = ['-creation_datetime']

    def __unicode__(self):
        return unicode("%s - %s" % (self.id, self.contents))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)

    @property
    def contents(self):
        return self._i_contents

    @property
    def multimedia_type(self):
        return self._i_multimedia_type

    @property
    def multimedia_url(self):
        return self._i_multimedia_url

    def convert_to_object(self):
        return {
            "post_id": self.id,
            "content": self.contents,
            "user_id": self.user_id,
            "article_id": self.article_id,
            "multimedia_type": self.multimedia_type,
            "multimedia_url": self.multimedia_url,
            "creation_datetime": self.creation_datetime
        }

    @staticmethod
    def get_post_object(post_id, req_user, access_token):
        language_name = VernacularUtilitiesClass.validate_language(language_name=req_user.language)[0]
        try:
            post = Post.objects.get(id=post_id)
        except:
            raise NotFound("Post is doesn't exits")
        post.set_language_specific_attributes(language_name=language_name)
        post_details = {
            "post_id": post.id,
            "contents": post.contents,
            "user_id": post.user_id,
            "article_id": post.article_id

        }
        return post_details

    @classmethod
    def add_post(cls, content=None, article_id=None, user=None, multimedia_type='', multimedia_url=''):
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]
        post = cls(_contents=content, article_id=article_id, user_id=user.id, _multimedia_type=multimedia_type,
                   _multimedia_url=multimedia_url)
        post.save()

        from ib_posts.models.post_vernacular_details import PostVernacularDetails
        PostVernacularDetails.objects.create(post_id=post.id, v_contents=post.contents, language_name=language_name,
                                             v_multimedia_type=multimedia_type, v_multimedia_url=multimedia_url)

        return {'post_id': post.id}

    @classmethod
    def update_post(cls, content=None, post_id=None, article_id=None, user=None):
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]

        try:
            post = cls.objects.get(id=post_id)
            if post.user_id != user.id:
                raise Forbidden('Write Forbidden', res_status='failed')
            post._contents = content
            post.article_id = article_id
            post.save()

            from ib_posts.models.post_vernacular_details import PostVernacularDetails
            try:
                pvd = PostVernacularDetails.objects.get(post=post, language_name=language_name)
                pvd.v_contents = post.contents
                pvd.save()
            except PostVernacularDetails.DoesNotExist:
                PostVernacularDetails.objects.create(post_id=post.id, v_contents=post.contents,
                                                     language_name=language_name)

        except cls.DoesNotExist:
            raise BadRequest('Post ID doesn\'t exist', res_status='failed')

    @classmethod
    def delete_post(cls, post_id=None, user=None):
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]

        try:
            post = cls.objects.get(id=post_id)
            if post.user_id != user.id:
                raise Forbidden('Write Forbidden', res_status='failed')

            from ib_posts.models.post_vernacular_details import PostVernacularDetails
            try:
                pvd = PostVernacularDetails.objects.get(post=post, language_name=language_name)
                pvd.delete()
            except PostVernacularDetails.DoesNotExist:
                pass
            post.delete()
        except cls.DoesNotExist:
            raise BadRequest('Post ID doesn\'t exist', res_status='failed')

    @classmethod
    def get_post_by_id(cls, post_id=None, user=None):
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]
        try:
            post = cls.objects.get(id=post_id)
        except:
            raise NotFound("Post is doesn't exits")
        post.set_language_specific_attributes(language_name=language_name)
        post_details = post.convert_to_object()
        return post_details

    @classmethod
    def get_post_by_id_with_article(cls, post_id=None, user=None, _adapter=None):
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]
        try:
            post = cls.objects.get(id=post_id)
        except:
            raise NotFound("Post is doesn't exits")
        post.set_language_specific_attributes(language_name=language_name)
        post_details = post.convert_to_object()

        article = None
        if post.article_id and post.article_id != -1:
            article = _adapter.ib_articles.get_article(post.article_id)
        post_details['article_info'] = article
        return post_details

    @classmethod
    def get_posts(cls, **request_data):

        access_token = request_data["access_token"]
        user = request_data['user']
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]

        from ib_posts.adapters.service_adapter import ServiceAdapter
        _adapter = ServiceAdapter(user=user, access_token=access_token)

        offset = request_data.get('offset', None)
        limit = request_data.get('limit', None)
        search_q = request_data.get('search_q', None)

        filters = request_data.get('filters', {})
        user_ids = filters.get('user_ids', [])
        post_ids = filters.get('post_ids', [])
        media_types = filters.get('media_types', [])
        include_article_info = filters.get("include_article_info", False)

        sorts = filters.get('sorts', None)
        if sorts:
            sort_by_date = sorts.get('sort_by_date', None)
        else:
            sort_by_date = None

        posts = cls.objects.all()
        if post_ids:
            posts = posts.filter(id__in=post_ids)
        if user_ids:
            posts = posts.filter(user_id__in=user_ids)
        if search_q:
            posts = posts.filter(vernacular_details__v_contents__icontains=search_q)
        if media_types:
            posts = posts.filter(vernacular_details__v_multimedia_type__in=media_types)

        return cls.get_posts_from_qs(posts, offset, limit, sort_by_date, language_name,
                                     include_article_info, _adapter)

    @classmethod
    def get_posts_from_qs(cls, posts, offset, limit, sort_by_date, language_name,
                          include_article_info, _adapter):
        if offset is None:
            offset = variables.OFFSET
        if limit is None:
            limit = variables.LIMIT
        if sort_by_date is "desc":
            posts = posts.order_by('-creation_datetime')

        posts = posts[offset:offset + limit]
        posts = posts.prefetch_related('vernacular_details')
        [post.set_language_specific_attributes(language_name=language_name) for post in posts]

        posts_list = []
        article_ids = []
        for post in posts:
            _dict = post.convert_to_object()

            article_id = _dict["article_id"]
            if article_id and article_id != -1:
                article_ids.append(_dict["article_id"])
            posts_list.append(_dict)

        if article_ids and include_article_info:
            articles_dict = cls.get_articles_dict_from_article_ids(article_ids, _adapter, offset, limit)
            for each_post in posts_list:
                each_post.update({"article_info": articles_dict.get(each_post["article_id"], {})})

        return posts_list

    @classmethod
    def get_articles_dict_from_article_ids(cls, article_ids, _adapter, offset, limit):
        articles = []
        if article_ids:
            articles = _adapter.ib_articles.get_article_by_ids(article_ids, offset, limit)
        articles_dict = dict()
        for each in articles:
            articles_dict[each["article_id"]] = each
        return articles_dict

    @classmethod
    def get_post_user_stats(cls, user_id):
        posts = cls.objects.filter(user_id=user_id).values('_multimedia_type').annotate(count=Count('_multimedia_type')).order_by('count')
        total = 0
        posts_media_type = []
        for each in posts:
            total += each["count"]
            _dict = {
                "multimedia_type": each["_multimedia_type"],
                "count": each["count"]
            }
            posts_media_type.append(_dict)
        return total, posts_media_type
