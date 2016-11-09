# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django_webp.views import index

urlpatterns = [
    url(r'^$', index),
] + staticfiles_urlpatterns()

# Only for test purposes
