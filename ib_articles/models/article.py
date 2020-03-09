from django.db import models
from django_swagger_utils.drf_server.exceptions.bad_request import BadRequest
from django_swagger_utils.drf_server.exceptions.forbidden import Forbidden
from django_swagger_utils.drf_server.exceptions.not_found import NotFound

from ib_articles.constants import variables
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel
from ib_common.vernacular_utils.vernacular_utilities_class import VernacularUtilitiesClass

from ib_articles.models.rss_feed import RSSFeed
from ib_articles.models.cluster import Cluster
from ib_articles.models.keyword import Keyword
from ib_articles.models.new_source import NewsSource


class Article(AbstractDateTimeModel, VernacularUtilitiesClass):
    _title = models.CharField(max_length=500)
    _url = models.CharField(max_length=600)
    _summary = models.TextField(max_length=100000000)
    _author_name = models.CharField(max_length=300)
    _published_time = models.DateTimeField(null=True)
    _tags = models.TextField(max_length=1000, null=True, blank=True)
    _image = models.CharField(max_length=1000, null=True, blank=True)
    keywords = models.ManyToManyField(Keyword, through='ArticleKeywordMap', related_name='articles')
    is_keywords_added = models.BooleanField(default=False)
    cluster = models.ForeignKey(Cluster, null=True, blank=True)
    news_source = models.ForeignKey(NewsSource, null=True, blank=True)
    rss_feed = models.ForeignKey(RSSFeed, null=True, blank=True)

    class Meta:
        app_label = 'ib_articles'
        ordering = ['-_published_time']

    def __unicode__(self):
        return unicode("%s - %s" % (self.id, self.title))

    def __unicode__(self):
        return str(self.id)
        
    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)

    @property
    def title(self):
        return self._i_title

    @property
    def url(self):
        return self._i_url

    @property
    def summary(self):
        return self._i_summary

    @property
    def author_name(self):
        return self._i_author_name

    @property
    def published_time(self):
        return self._i_published_time

    @property
    def tags(self):
        return self._i_tags

    @property
    def image(self):
        return self._i_image

    @property
    def to_dict(self):

        news_source = None

        news_source_obj = self.news_source
        if news_source_obj is not None:
            news_source = {
                "name": news_source_obj.name,
                "url": news_source_obj.url
            }

        article_details = {
            "title": self.title,
            "article_id": self.id,
            "url": self.url,
            "summary": self.summary,
            "author_name": self.author_name,
            "published_time": self.published_time,
            "tags": self.tags,
            "image": self.image,
            "news_source": news_source,
            "keywords": self.get_article_keywords

        }
        return article_details

    @classmethod
    def get_article_by_url(cls, user, url):
        articles = cls.objects.filter(_url=url)
        return cls.get_articles_from_objects(articles, 0, 10, user.language)

    @property
    def get_article_keywords(self):
        keywords = self.keywords.all()
        keywords_list = []
        for each_keyword in keywords:
            each_keyword.set_language_specific_attributes()
            keywords_list.append({"keyword": each_keyword.keyword, 'keyword_id': each_keyword.id})
        return keywords_list

    @staticmethod
    def get_article_object(article_id, req_user, access_token):
        language_name = VernacularUtilitiesClass.validate_language(language_name=req_user.language)[0]
        try:
            article = Article.objects.get(id=article_id)
        except:
            from django_swagger_utils.drf_server.exceptions.not_found import NotFound
            raise NotFound("Article is doesn't exits")
        article.set_language_specific_attributes(language_name=language_name)
        return article.to_dict

    @classmethod
    def add_article(cls, title=None, summary=None, url=None, user=None, author_name=None, published_time=None,
                    tags=None, image=None, news_source_id=None):
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]

        if not user.is_staff:
            raise Forbidden('Write access forbidden', res_status='failed')

        article = cls(_title=title, _summary=summary, _url=url, _published_time=published_time,
                      _author_name=author_name, _tags=tags, _image=image, news_source_id=news_source_id, )

        article.save()

        from ib_articles.models.article_vernacular_details import ArticleVernacularDetails
        ArticleVernacularDetails.objects.create(language_name=language_name,
                                                article=article,
                                                v_title=title,
                                                v_summary=summary,
                                                v_url=url,
                                                v_published_time=published_time,
                                                v_author_name=author_name,
                                                v_tags=tags,
                                                v_image=image)
        return {'article_id': article.id}

    @classmethod
    def get_article_by_id(cls, article_id=None, user=None):
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]
        try:
            article = cls.objects.get(id=article_id)
            article.set_language_specific_attributes(language_name=language_name)
            return article.to_dict
        except Exception, err:
            print err
            raise BadRequest('Article not found', res_status='failed')

    @classmethod
    def get_articles(cls, user=None, offset=None, limit=None, search_q=None, sort_by_date=None):
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]

        if offset is None:
            offset = variables.OFFSET

        if limit is None:
            limit = variables.LIMIT

        articles = cls.objects.all()
        if sort_by_date is "desc":
            articles.order_by('-_published_time')
        if search_q:
             articles = articles.filter(_title__icontains = search_q)
        return cls.get_articles_from_objects(articles, offset, limit, language_name)

    @staticmethod
    def get_keywords_dict(article_ids, language_name):
        from ib_articles.models import KeywordVernacularDetails
        keywords = KeywordVernacularDetails.objects.filter(
            language_name=language_name,
            keyword__articles__id__in=article_ids
        ).values(
            'v_keyword',
            'keyword__articles__id'
        )

        keywords_dict = dict()
        for each in keywords:
            if each['keyword__articles__id'] not in keywords_dict:
                keywords_dict[each['keyword__articles__id']] = [each['v_keyword']]
            else:
                keywords_dict[each['keyword__articles__id']].append(each['v_keyword'])
        return keywords_dict

    @staticmethod
    def convert_vernacular_article(vernacular_article_dict):
        article = {
            'news_source': {
                'name': vernacular_article_dict['article__news_source__name'],
                'url': vernacular_article_dict['article__news_source__url']
            },
            'title': vernacular_article_dict['v_title'],
            'url': vernacular_article_dict['v_url'],
            'summary': vernacular_article_dict['v_summary'],
            'author_name': vernacular_article_dict['v_author_name'],
            'published_time': vernacular_article_dict['v_published_time'],
            'tags': vernacular_article_dict['v_tags'],
            'image': vernacular_article_dict['v_image'],
            'article_id': vernacular_article_dict['article_id']
        }
        return article

    @classmethod
    def get_articles_v2(cls, user=None, offset=None, limit=None, search_q=None, sort_by_date=None):
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]

        if offset is None:
            offset = variables.OFFSET

        if limit is None:
            limit = variables.LIMIT

        from ib_articles.models import ArticleVernacularDetails
        vernacular_articles = ArticleVernacularDetails.objects.filter(language_name=language_name)
        total = vernacular_articles.count()
        if sort_by_date is "desc":
            vernacular_articles.order_by('-v_published_time')

        vernacular_articles = vernacular_articles[offset:offset + limit]
        vernacular_articles = vernacular_articles.values(
            'article__news_source__name',
            'article__news_source__url',
            'v_title',
            'v_url',
            'v_summary',
            'v_author_name',
            'v_published_time',
            'v_tags',
            'v_image',
            'article_id'
        )
        article_ids = [each['article_id'] for each in vernacular_articles]
        keywords_dict = cls.get_keywords_dict(article_ids, language_name)
        articles_dict = []
        for each in vernacular_articles:
            _dict = cls.convert_vernacular_article(each)
            _dict['keywords'] = keywords_dict.get(_dict['article_id'], [])
            articles_dict.append(_dict)
        response = {
            'total': total,
            'articles': articles_dict
        }
        return response

    @classmethod
    def update_article(cls, user=None, article_id=None, title=None, summary=None, url=None, author_name=None,
                       published_time=None, tags=None, image=None, news_source_id=None):
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]

        try:
            article = cls.objects.get(id=article_id)
            if not user.is_staff:
                raise Forbidden('Write access forbidden', res_status='failed')

            if title:
                article._title = title

            if summary:
                article._summary = summary

            if url:
                article._url = url

            if author_name:
                article.author_name = author_name

            if published_time:
                article.published_time = published_time

            if tags:
                article._tags = tags
            if image:
                article._image = image
            if news_source_id:
                article.news_source_id = news_source_id

            from ib_articles.models.article_vernacular_details import ArticleVernacularDetails
            try:
                avd = ArticleVernacularDetails.objects.get(language_name=language_name, article=article)
                avd.v_title = article.title
                avd.v_summary = article.summary
                avd.v_author_name = article.author_name
                avd.v_published_time = article.published_time
                avd.v_url = article.url
                avd.v_tags = article.tags
                avd.v_image = article.image
                avd.save()
            except ArticleVernacularDetails.DoesNotFound:
                ArticleVernacularDetails.objects.create(language_name=language_name,
                                                        article=article,
                                                        v_title=title,
                                                        v_summary=summary,
                                                        v_url=url,
                                                        v_published_time=published_time,
                                                        v_author_name=author_name,
                                                        v_tags=tags,
                                                        v_image=image)

            article.save()
            return
        except Article.DoesNotExist:
            raise BadRequest('Article not found', res_status='failed')

    @classmethod
    def delete_article(cls, article_id=None, user=None):
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]

        try:
            article = cls.objects.get(id=article_id)
            if not user.is_staff:
                raise Forbidden('Write access forbidden', res_status='failed')

            from ib_articles.models.article_vernacular_details import ArticleVernacularDetails
            try:
                avd = ArticleVernacularDetails.objects.get(language_name=language_name, article=article)
                avd.delete()
            except ArticleVernacularDetails.DoesNotFound:
                pass
            article.delete()
            return
        except Article.DoesNotExist:
            raise BadRequest('Article not found', res_status='failed')

    @classmethod
    def get_article_by_ids(cls, user, article_ids, offset, limit, sort_by_published_date, search_q):
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]

        articles = cls.objects.filter(pk__in=article_ids)
        clauses = ' '.join(['WHEN %s.id=%s THEN %s' % (articles.model._meta.db_table, pk, i) for i, pk in
                            enumerate(article_ids)])
        ordering = 'CASE %s END' % clauses
        articles = articles.extra(select={'ordering': ordering}, order_by=('ordering',))

        if sort_by_published_date is "desc":
            articles = articles.order_by('ordering', '-creation_datetime')

        return cls.get_articles_from_objects(articles, offset, limit, language_name)

    @classmethod
    def get_articles_from_objects(cls, articles, offset, limit, language_name):
        if limit>0:
            articles = articles[offset:offset + limit]
        articles = list(articles.select_related('news_source').prefetch_related('vernacular_details',
                                                                                'keywords__vernacular_details'))
        [article.set_language_specific_attributes(language_name=language_name) for article in articles]
        articles_list = [article.to_dict for article in articles]
        return articles_list

    @property
    def to_basic_dict(self):
        article_details = {
            "title": self.title,
            "article_id": self.id,
            "url": self.url,
            "summary": self.summary,
            "author_name": self.author_name,
            "published_time": self.published_time,
            "tags": self.tags,
            "image": self.image,
        }
        return article_details

    @classmethod
    def get_basic_articles(cls, user, article_ids, sort_by_published_date, end_published_time, start_published_time):
        language_name = VernacularUtilitiesClass.validate_language(language_name=user.language)[0]
        articles = cls.objects.filter(vernacular_details__language_name=language_name)
        if article_ids:
            articles = articles.filter(id__in=article_ids)
        if end_published_time:
            articles = articles.filter(vernacular_details__v_published_time__lte=end_published_time)
        if start_published_time:
            articles = articles.filter(vernacular_details__v_published_time__gte=start_published_time)
        if sort_by_published_date is "desc":
            articles.order_by('-creation_datetime')
        articles = list(articles.prefetch_related('vernacular_details'))
        [article.set_language_specific_attributes(language_name=language_name) for article in articles]
        articles_list = [article.to_basic_dict for article in articles]
        return articles_list

