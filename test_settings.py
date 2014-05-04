# -*- coding: utf-8 -*-

SECRET_KEY = 'psst'
SITE_ID = 1

ROOT_URLCONF = 'styleguide.urls'

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
    'styleguide',
    'styleguide_mock',
)