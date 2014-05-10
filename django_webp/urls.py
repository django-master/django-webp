# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('django_webp.views',
    url(r'^$', 'index'),
) + staticfiles_urlpatterns()

# Only for test purposes
