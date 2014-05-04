# -*- coding: utf-8 -*-
from django import template
from django.conf import settings


register = template.Library()
WEBP_URL = getattr(settings, 'WEBP_URL', '/webp')


@register.simple_tag()
def webp(value):
    return "%s/%s" % (WEBP_URL, value)