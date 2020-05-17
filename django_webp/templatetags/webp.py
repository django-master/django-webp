# -*- coding: utf-8 -*-
import os
import logging
from PIL import Image

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.templatetags.static import static

from django_webp.utils import (WEBP_STATIC_URL, WEBP_STATIC_ROOT, WEBP_DEBUG, WEBP_CONVERT_MEDIA_FILES,
                               WEBP_STATIC_ROOT, WEBP_MEDIA_ROOT, WEBP_MEDIA_URL)

register = template.Library()


def get_static_image(image_url):
    return static(image_url)


class WEBPImageConverter:

    def generate_path(self, image_path):
        """ creates all folders necessary until reach the file's folder """
        folder_path = os.path.dirname(image_path)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)


    def get_generated_image(self, image_url):
        """ Returns the url to the webp gerenated image,
        if the image doesn't exist or the generetion fails,
        it returns the regular static url for the image """
        real_url = os.path.splitext(image_url)[0] + '.webp'
        generated_path = os.path.join(WEBP_STATIC_ROOT, real_url)
        real_url = WEBP_STATIC_URL + real_url

        image_path = finders.find(image_url)
        if not image_path:
            return get_static_image(image_url)

        if not self.generate_webp_image(generated_path, image_path):
            return get_static_image(image_url)
        return real_url

    def generate_webp_image(self, generated_path, image_path):
        if os.path.isfile(generated_path):
            return True

        image = Image.open(image_path)
        try:
            self.generate_path(generated_path)
            image.save(generated_path, 'WEBP')
            return True
        except KeyError:
            logger = logging.getLogger(__name__)
            logger.warn('WEBP is not installed in pillow')
            return False
        except (IOError, OSError):
            logger = logging.getLogger(__name__)
            logger.warn('WEBP image could not be saved in %s' % generated_path)
            return False


class WEBPMediaImageConverter(WEBPImageConverter):
    def get_generated_image(self, image_url):
        image_path = image_url.replace(settings.MEDIA_URL, settings.MEDIA_ROOT)

        if not os.path.isfile(image_path):
            return image_url

        real_url = os.path.splitext(image_url)[0] + '.webp'
        generated_path = self.join_path(WEBP_MEDIA_ROOT, real_url)

        if not self.generate_webp_image(generated_path, image_path):
            return get_static_image(image_url)


        if WEBP_MEDIA_URL.endswith('/'):
            return WEBP_MEDIA_URL[:-1] + real_url
        else:
            return WEBP_MEDIA_URL + real_url

    def join_path(self, *names):
        result = []

        for name in names:
            if name.endswith(os.path.sep):
                name = name[:-1]
            if name.startswith(os.path.sep):
                name = name[1:]
            result.append(name)

        return os.path.sep + os.path.join(*result)


def _join_path(*names):
    result = []

    for name in names:
        if name.endswith(os.path.sep):
            name = name[:-1]
        if name.startswith(os.path.sep):
            name = name[1:]
        result.append(name)

    return os.path.join(*result)


def _join_url(*names):
    result = []

    for name in names:
        if name.endswith('/'):
            name = name[:-1]
        if name.startswith('/'):
            name = name[1:]
        result.append(name)

    return '/' + '/'.join(result)


@register.simple_tag(takes_context=True)
def webp(context, value, force_static=WEBP_DEBUG):
    supports_webp = context.get('supports_webp', False)
    if not supports_webp or force_static:
        return get_static_image(value)

    is_mediafile = WEBP_CONVERT_MEDIA_FILES and value.startswith(settings.MEDIA_URL)
    if is_mediafile:
        return WEBPMediaImageConverter().get_generated_image(value)
    else:
        return WEBPImageConverter().get_generated_image(value)
