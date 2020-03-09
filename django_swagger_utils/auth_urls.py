# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login

urlpatterns = [
    url(r"^login/$", login, {"template_name": "login.html"}, name="django.contrib.auth.views.login"),
    url(r"^logout/$", logout_then_login, name="logout"),
]
