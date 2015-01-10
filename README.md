django-webp
===========

Returns a webp image instead of jpg, gif or png to browsers which have support.

[![Build Status](https://travis-ci.org/andrefarzat/django-webp.png?branch=master)](https://travis-ci.org/andrefarzat/django-webp)
[![Coverage Status](https://coveralls.io/repos/andrefarzat/django-webp/badge.png)](https://coveralls.io/r/andrefarzat/django-webp)
[![Requirements Status](https://requires.io/github/andrefarzat/django-webp/requirements.png?branch=master)](https://requires.io/github/andrefarzat/django-webp/requirements/?branch=master)


## Usage

Load the `webp` module in your template and use the `webp` templatetag to point
to the image you want to convert.

```html
{% load webp %}

{# Use webp as you would use static templatetag #}
<img src="{% webp 'path/to/your/image.png' %}" alt="image" />
<!--
If the browser has support, generates:
<img src="/static/WEBP_CACHE/path/to/your/image.webp" alt="image" />

else, generates:
<img src="/static/path/to/your/image.png" alt="image" />
-->
```


## Installation

First of all, you must install the webp support. In ubuntu you can install via apt-get:
```sh
apt-get install libwebp-dev
```
Please, check [the official guide](https://developers.google.com/speed/webp/docs/precompiled) for the other systems.


Then, install `django-webp`.
```sh
pip install django-webp
```

add it to `INSTALLED_APPS` configuration

```python
INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django_webp',
    '...',
)
```

and to `TEMPLATE_CONTEXT_PROCESSORS`  configuration

```python
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.static",
    "django_webp.context_processors.webp",
    "...",
)
```


## Possible problems

`django-webp` uses `Pillow` to convert the images. If you've installed the `libwebp-dev` after already installed `Pillow`,
it's necessary to uninstall and install it back because it needs to be compiled with it.


## Cleaning the cache

You can clean the cache running:
```sh
python manage.py clean_webp_images
```
