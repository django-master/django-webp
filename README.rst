django-webp
===========

Returns a webp image instead of jpg, gif or png to browsers which have
support.

|Build Status| |Coverage Status|


Usage
-----

Load the ``webp`` module in your template and use the ``webp``
templatetag to point to the image you want to convert.

.. code:: html

    {% load webp %}

    {# Use webp as you would use static templatetag #}
    <img src="{% webp 'path/to/your/image.png' %}" alt="image" />
    <!--
    If the browser has support, generates:
    <img src="/static/WEBP_CACHE/path/to/your/image.webp" alt="image" />

    else, generates:
    <img src="/static/path/to/your/image.png" alt="image" />
    -->

Installation
------------

First, if you are using a version of Pillow <= 9.3.0, you must install  webp support since earlier versions of Pillow do not 
have webp support built-in. In ubuntu, you can install via apt-get:

.. code:: sh

    apt-get install libwebp-dev

Please, check `the official guide`_ for the other systems.

Then, install ``django-webp``.

.. code:: sh

    pip install django-webp

add it to ``INSTALLED_APPS`` configuration

.. code:: python

    INSTALLED_APPS = (
        'django.contrib.staticfiles',
        'django_webp',
        '...',
    )

add the django\_webp context processor

.. code:: python

    TEMPLATES = [
        {
            '...'
            'OPTIONS': {
                'context_processors': [
                    '...',
                    'django_webp.context_processors.webp',
                ],
            },
        },
    ]

Settings
--------

The following Django-level settings affect the behavior of the library

- ``WEBP_CHECK_URLS``

  When set to ``True``, urls that link to externally stored images (i.e. images hosted by another site) are checked to confirm if they are valid image links.
  Ideally, this should temporarily be set to ``True`` whenever the ``WEBP_CACHE`` has been cleaned or if there has been substantial changes to your project's template files.
  This defaults to ``False``.

- ``USING_WHITENOISE``

  Set to ``True`` when whitenoise is used as middleware, defaults to ``False`` if not. Used to determine the directory to store the ``WEBP_CACHE``.


Possible problems
-----------------

- ``django-webp`` uses ``Pillow`` to convert the images. If you’ve installed the ``libwebp-dev`` after already installed ``Pillow``, it’s necessary to uninstall and install it back because it needs to be compiled with it.

Cleaning the cache
------------------

You can clean the cache running:

.. code:: sh

    python manage.py clean_webp_images

.. _the official guide: https://developers.google.com/speed/webp/docs/precompiled

.. |Build Status| image:: https://github.com/andrefarzat/django-webp/actions/workflows/django.yml/badge.svg?branch=master
   :target: https://github.com/andrefarzat/django-webp/actions/workflows/django.yml
.. |Coverage Status| image:: https://coveralls.io/repos/github/andrefarzat/django-webp/badge.svg?branch=master
   :target: https://coveralls.io/github/andrefarzat/django-webp?branch=master
