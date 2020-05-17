import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static


STATIC_ROOT = getattr(settings, 'STATIC_ROOT', '') or ''

WEBP_STATIC_ROOT = getattr(settings, 'WEBP_STATIC_ROOT', 'WEBP_CACHE')
WEBP_STATIC_ROOT = STATIC_ROOT + WEBP_STATIC_ROOT

WEBP_STATIC_URL = static(getattr(settings, 'WEBP_STATIC_URL', 'WEBP_CACHE/'))


WEBP_DEBUG = getattr(settings, 'WEBP_DEBUG', settings.DEBUG)


WEBP_CONVERT_MEDIA_FILES = getattr(settings, 'WEBP_CONVERT_MEDIA_FILES', False)


if not WEBP_STATIC_URL.endswith('/'):
    raise ImproperlyConfigured("If set, WEBP_STATIC_URL must end with a slash")