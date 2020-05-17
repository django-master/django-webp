# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static


STATIC_ROOT = getattr(settings, 'STATIC_ROOT', '') or ''

WEBP_STATIC_ROOT = getattr(settings, 'WEBP_STATIC_ROOT', 'WEBP_CACHE')
WEBP_STATIC_ROOT = STATIC_ROOT + WEBP_STATIC_ROOT

WEBP_STATIC_URL = static(getattr(settings, 'WEBP_STATIC_URL', 'WEBP_CACHE/'))


WEBP_MEDIA_ROOT = getattr(settings, 'WEBP_MEDIA_ROOT', 'WEBP_MEDIA_CACHE')
WEBP_MEDIA_ROOT = STATIC_ROOT + WEBP_MEDIA_ROOT


WEBP_MEDIA_URL = static(getattr(settings, 'WEBP_MEDIA_URL', 'WEBP_MEDIA_CACHE'))

if WEBP_MEDIA_URL.endswith('/'):
    WEBP_MEDIA_URL = WEBP_MEDIA_URL[:-1]



WEBP_DEBUG = getattr(settings, 'WEBP_DEBUG', settings.DEBUG)


WEBP_CONVERT_MEDIA_FILES = getattr(settings, 'WEBP_CONVERT_MEDIA_FILES', False)


if WEBP_CONVERT_MEDIA_FILES and settings.MEDIA_URL == '':
    raise ImproperlyConfigured("When WEBP_CONVERT_MEDIA_FILES is True, MEDIA_URL must *not* be an empty string")


if not WEBP_STATIC_URL.endswith('/'):
    raise ImproperlyConfigured("If set, WEBP_STATIC_URL must end with a slash")