from django.contrib import admin

from ib_recommender.models import Category
from ib_recommender.models import CategoryVernacularDetails
from ib_recommender.models import UserActionMap
from ib_recommender.models import UserCategoryMap
from ib_recommender.models import UserKeywordMap

admin.site.register(Category)
admin.site.register(CategoryVernacularDetails)
admin.site.register(UserActionMap)
admin.site.register(UserCategoryMap)
admin.site.register(UserKeywordMap)
