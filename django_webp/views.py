# -*- coding: utf-8 -*-
import httpagentparser
import imghdr
import logging

from PIL import Image
from StringIO import StringIO

from django.http import HttpResponse, Http404
from django.contrib.staticfiles import finders

logger = logging.getLogger(__name__)

VALID_BROWSERS = ['Chrome', 'Opera', 'Opera Mobile']

def _return_static_image(image_path, content_type=None):
    if not content_type:
        content_type = "image/%s" % imghdr.what(image_path)

    image = open(image_path)
    return HttpResponse(image.read(), content_type=content_type)


def _return_webp_image(image_path):
    data = StringIO()
    image = Image.open(image_path)
    try:
        image.save(data, 'WEBP')
    except KeyError:
        logger.warn('WEBP is not installed in pillow')
        return _return_static_image(image_path)

    return HttpResponse(data.getvalue(), content_type="image/webp")


def _is_valid_browser(user_agent):
    if user_agent:
        data = httpagentparser.detect(user_agent)
        if 'browser' in data:
            return data['browser']['name'] in VALID_BROWSERS

    return False


def index(request, image_path=""):
    image = finders.find(image_path)
    if not image:
        raise Http404()

    user_agent = request.META.get('HTTP_USER_AGENT')
    if not _is_valid_browser(user_agent):
        return _return_static_image(image_path)

    return _return_webp_image(image)



    
