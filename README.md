django-webp
===========

webp middleware for django


## Installation

```sh
pip install django-wep
```

add it to `INSTALLED_APPS` configuration

```python
INSTALLED_APPS = ('django_webp', ...)
```

## Usage

There are two possible ways: Adding the middleware or by templatetag.

### Middleware

Add the `django_webp.middleware.` class to `MIDDLEWARE_CLASSES` configuration.
It is important to let it as the *last* class in the list.

```python
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    '...',
    'django_webp.middleware.Webp',
)
```


### Templatetag

It is necessary to set up the urls to use the templatetag.

```python
# urls.py

urlpatterns = patterns(
    url(r'^/webp', 'django_webp.views.webp', name="webp"),
)
```

Load the `webp` module in your template and use the `webp` templatetag to point
to the image you want to convert.

```django
{% load webp %}

{# Use webp as you would use static templatetag #}
<img src="{% webp 'path/to/your/image.png' %}" alt="image" />
<!-- produces:
<img src="/webp/path/to/your/image.png" alt="image" />
-->
```
