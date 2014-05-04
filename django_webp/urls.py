# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('django_webp.views',
    url(r'(?P<image_path>.+)', 'index', name="django_webp"),
)
