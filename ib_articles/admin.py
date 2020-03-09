from django.contrib import admin

from ib_articles.models import *

__author__ = 'tanmay.ibhubs'

admin.site.register(Article)
admin.site.register(ArticleVernacularDetails)
admin.site.register(ArticleKeywordMap)
admin.site.register(Cluster)
admin.site.register(Keyword)
admin.site.register(KeywordGroup)
admin.site.register(KeywordVernacularDetails)
admin.site.register(NewsSource)
