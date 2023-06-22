# -*- coding: utf-8 -*-
import os
import logging
from PIL import Image

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.templatetags.static import static

from django_webp.utils import WEBP_STATIC_URL, WEBP_STATIC_ROOT, WEBP_DEBUG, WEBP_CONVERT_MEDIA_FILES


register = template.Library()


class WEBPImageConverter:

    def generate_path(self, image_path):
        """ creates all folders necessary until reach the file's folder """
        folder_path = os.path.dirname(image_path)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

    def get_static_image(self, image_url):
        return static(image_url)

    def get_generated_image(self, image_url):
        """ Returns the url to the webp gerenated image,
        if the image doesn't exist or the generetion fails,
        it returns the regular static url for the image """
        real_url = os.path.splitext(image_url)[0] + '.webp'
        generated_path = os.path.join(WEBP_STATIC_ROOT, real_url)
        real_url = WEBP_STATIC_URL + real_url

        image_path = finders.find(image_url)
        if not image_path:
            return self.get_static_image(image_url)

        if not self.generate_webp_image(generated_path, image_path):
            return self.get_static_image(image_url)
        return real_url

    def generate_webp_image(self, generated_path, image_path):
        if os.path.isfile(generated_path):
            return True

        try:
            image = Image.open(image_path)
        except FileNotFoundError:
            return False

        try:
            self.generate_path(generated_path)
            image.save(generated_path, 'WEBP')
            return True
        except KeyError:
            logger = logging.getLogger(__name__)
            logger.warn('WEBP is not installed in pillow')
        except (IOError, OSError):
            logger = logging.getLogger(__name__)
            logger.warn('WEBP image could not be saved in %s' % generated_path)

        return False


@register.simple_tag(takes_context=True)
def webp(context, value, force_static=WEBP_DEBUG):
    converter = WEBPImageConverter()

    supports_webp = context.get('supports_webp', False)
    if not supports_webp or force_static:
        return converter.get_static_image(value)

    return converter.get_generated_image(value)
