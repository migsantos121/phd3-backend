from django.db import models
from django.utils import timezone

class NewsSource(models.Model):
    url = models.CharField(max_length=600)
    name = models.CharField(max_length=600)
    function_name = models.CharField(max_length=100)
    first_crawl = models.BooleanField(default=False)
    has_rss = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)
    date_crawled = models.DateTimeField()

    def __str__(self):
        return self.url

class Category(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class RssSource(models.Model):
    news_source = models.ForeignKey(NewsSource)
    category = models.ForeignKey(Category)
    rss_url = models.CharField(max_length=600)
    function_name = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=timezone.now)
    date_crawled = models.DateTimeField()

    def __str__(self):
        return self.rss_url

class Keyword_From_Source(models.Model):
    name = models.CharField(max_length=300)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class EntityType(models.Model):
    name = models.CharField(max_length=400)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Entity(models.Model):
    name = models.CharField(max_length=400)
    entity_type = models.ForeignKey(EntityType)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class RelationType(models.Model):
    name = models.CharField(max_length=400)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Relation(models.Model):
    name = models.CharField(max_length=400)
    relation_type = models.ForeignKey(RelationType)
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

class SocialTag(models.Model):
    name = models.CharField(max_length=400)
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

class Industry(models.Model):
    name = models.CharField(max_length=400)
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=400)
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=400)
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name


class Article(models.Model):
    news_source = models.ForeignKey(NewsSource)
    rss_source = models.ForeignKey(RssSource)
    
    # category_id = models.ManyToManyField(Category)
    keyword = models.ManyToManyField(Keyword_From_Source)
    entity = models.ManyToManyField(Entity, through='Article_Entity')
    relation = models.ManyToManyField(Relation)
    social_tag = models.ManyToManyField(SocialTag, through='Article_Social')
    industry = models.ManyToManyField(Industry, through='Article_Industry')
    topic = models.ManyToManyField(Topic, through='Article_Topic')
    language = models.ManyToManyField(Language)

    title = models.CharField(max_length=300)
    author_name = models.CharField(max_length=200)
    image = models.CharField(max_length=600)
    link = models.CharField(max_length=600)
    summary = models.TextField()
#     article_date = models.DateTimeField()
    slug = models.CharField(max_length=300)
    date_crawled = models.DateTimeField(default=timezone.now)
    publish_date = models.DateTimeField()
    article_id = models.CharField(max_length=12)
    
    def __str__(self):
        return self.link

class ArticleDescription(models.Model):
    article = models.ForeignKey(Article)
    description = models.TextField()
    status = models.BooleanField(default=False)
    date_crawled = models.DateTimeField(default=timezone.now)
    
class Article_Entity(models.Model):
    article = models.ForeignKey(Article)
    entity = models.ForeignKey(Entity)
    relevance = models.FloatField()
    date_added = models.DateTimeField(default=timezone.now)
    
class Article_Social(models.Model):
    article = models.ForeignKey(Article)
    social_tag = models.ForeignKey(SocialTag)
    relevance = models.FloatField()
    date_added = models.DateTimeField(default=timezone.now)

class Article_Industry(models.Model):
    article = models.ForeignKey(Article)
    industry = models.ForeignKey(Industry)
    relevance = models.FloatField()
    permid = models.FloatField()
    date_added = models.DateTimeField(default=timezone.now)
    
class Article_Topic(models.Model):
    article = models.ForeignKey(Article)
    topic = models.ForeignKey(Topic)
    relevance = models.FloatField()
    date_added = models.DateTimeField(default=timezone.now)
    
class Calais(models.Model):
    article = models.ForeignKey(Article)
    calais_request_id = models.CharField(max_length=300)
    calais_id = models.CharField(max_length=300)
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
