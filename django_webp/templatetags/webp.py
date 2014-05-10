# -*- coding: utf-8 -*-
import os
import logging
from PIL import Image

from django import template
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.templatetags.staticfiles import static

from django_webp.utils import WEBP_STATIC_URL, WEBP_STATIC_ROOT, WEBP_DEBUG

register = template.Library()


def _get_static_image(image_url):
    return static(image_url)


def _generate_path(image_path):
    """ creates all folders necessary until reach the file's folder """
    current_path = ''
    image_path = list(image_path.split('/'))
    image_path.reverse()

    while image_path:
        current_path = os.path.join(current_path, image_path.pop())
        if os.path.isdir(current_path):
            continue

        if image_path:
            # if isn't the last one
            os.mkdir(current_path)


def _generate_webp_image(image_path, image_url):
    real_url = os.path.splitext(image_url)[0] + '.webp'
    generated_path = os.path.join(WEBP_STATIC_ROOT, real_url)
    real_url = WEBP_STATIC_URL + real_url

    if not os.path.isfile(generated_path):
        # generating the image
        image = Image.open(image_path)
        try:
            _generate_path(generated_path)
            image.save(generated_path, 'WEBP')
        except KeyError:
            logger = logging.getLogger(__name__)
            logger.warn('WEBP is not installed in pillow')
            return _get_static_image(image_url)
        except (IOError, OSError):
            logger = logging.getLogger(__name__)
            logger.warn('WEBP image could not be saved in %s' % real_url)
            return _get_static_image(image_url)

    return real_url


def _get_generated_image(image_url):
    """ Returns the url to the webp gerenated image,
        if the image doesn't exist or the generetion fails,
        it returns the regular static url for the image """

    image_path = finders.find(image_url)
    if not image_path:
        return _get_static_image(image_url)

    return _generate_webp_image(image_path, image_url)


@register.simple_tag(takes_context=True)
def webp(context, value, force_static=WEBP_DEBUG):
    supports_webp = context.get('supports_webp', False)
    if not supports_webp or force_static:
        return _get_static_image(value)
    else:
        return _get_generated_image(value)
