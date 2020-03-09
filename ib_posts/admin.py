from django.contrib import admin

from ib_posts.models.post import Post
from ib_posts.models.post_vernacular_details import PostVernacularDetails

__author__ = 'tanmay.ibhubs'

admin.site.register(Post)
admin.site.register(PostVernacularDetails)
