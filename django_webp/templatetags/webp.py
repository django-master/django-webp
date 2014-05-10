# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse


register = template.Library()

@register.simple_tag(takes_context=True)
def webp(context, value):
    return reverse("django_webp", args=(value, ))