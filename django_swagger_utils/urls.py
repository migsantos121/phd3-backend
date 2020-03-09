# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^chartit/',views.chartit,name='chartit'),
    url(r'^(?P<path>.*)/?$', views.swagger_ui, name='swagger_ui'),
]
