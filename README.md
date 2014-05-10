django-webp
===========

webp middleware for django

[![Build Status](https://travis-ci.org/andrefarzat/django-webp.png?branch=master)](https://travis-ci.org/andrefarzat/django-webp)
[![Coverage Status](https://coveralls.io/repos/andrefarzat/django-webp/badge.png)](https://coveralls.io/r/andrefarzat/django-webp)
[![Requirements Status](https://requires.io/github/andrefarzat/django-webp/requirements.png?branch=master)](https://requires.io/github/andrefarzat/django-webp/requirements/?branch=master)


Returns a webp image instead of jpg, gif or png to browsers which have support.

## Installation

First of all, you must install the webp support.
Please, check [the official guide](https://developers.google.com/speed/webp/docs/precompiled).

Then, install `django-webp`.

```sh
pip install django-webp
```

add it to `INSTALLED_APPS` configuration

```python
INSTALLED_APPS = ('django_webp', ...)
```

## Usage

Load the `webp` module in your template and use the `webp` templatetag to point
to the image you want to convert.

```html
{% load webp %}

{# Use webp as you would use static templatetag #}
<img src="{% webp 'path/to/your/image.png' %}" alt="image" />
<!-- produces:
<img src="/static/CACHE/webp/path/to/your/image.webp" alt="image" />
-->
```
