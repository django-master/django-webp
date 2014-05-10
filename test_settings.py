# -*- coding: utf-8 -*-

ALLOWED_HOSTS = ['*']
DEBUG = False
SECRET_KEY = 'psst'
SITE_ID = 1

ROOT_URLCONF = 'django_webp.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}


INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django_webp',
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.static",
    "django_webp.context_processors.webp",
)