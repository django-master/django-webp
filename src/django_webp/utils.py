import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static


USING_WHITENOISE = "whitenoise.middleware.WhiteNoiseMiddleware" in settings.MIDDLEWARE

STATIC_ROOT = getattr(settings, "STATIC_ROOT", "") or ""

WEBP_CHECK_URLS = getattr(settings, "WEBP_CHECK_URLS", "") or False

WEBP_STATIC_ROOT = getattr(settings, "WEBP_STATIC_ROOT", "WEBP_CACHE")
WEBP_STATIC_ROOT = os.path.join(STATIC_ROOT, WEBP_STATIC_ROOT)
WEBP_STATIC_URL = static(getattr(settings, "WEBP_STATIC_URL", "WEBP_CACHE/"))

WEBP_DEBUG = getattr(settings, "WEBP_DEBUG", settings.DEBUG)

if not WEBP_STATIC_URL.endswith("/"): # pragma: no cover
    raise ImproperlyConfigured("If set, WEBP_STATIC_URL must end with a slash")
