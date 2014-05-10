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
    'django_webp',
)

STATIC_URL = 'static/'