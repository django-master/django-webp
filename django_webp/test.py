# -*- coding: utf-8 -*-
import unittest

from PIL import Image
from StringIO import StringIO

from django.template import Template, Context
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.staticfiles import finders

from django_webp.templatetags.webp import webp


USER_AGENTS = [
    # Chrome
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',

    # Opera
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    'Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52',
]

IMAGE_PNG_PATH = finders.find('django_webp/python.png')
IMAGE_WEBP_PATH = finders.find('django_webp/python.webp')

CONVERTED_IMAGE = None

def _get_converted_image():
    global CONVERTED_IMAGE

    if CONVERTED_IMAGE is None:
        CONVERTED_IMAGE = StringIO()
        image = Image.open(IMAGE_PNG_PATH)
        image.save(CONVERTED_IMAGE, 'webp')

    return CONVERTED_IMAGE


class MainTest(unittest.TestCase):

    def test_pillow(self):
        """ Checks if current pillow installation
        has support to WEBP """
        image = Image.open(IMAGE_PNG_PATH)
        try:
            image.load()
            self.assertTrue(True)
        except:
            self.assertTrue(False, "There is no support for webp")


class TemplateTagTest(unittest.TestCase):

    def setUp(self):
        self.expected = reverse('django_webp', args=('path/to/the/image.png', ))

    def render_template(self, html, context={}):
        return Template(html).render(Context(context))

    def test_templatetag(self):
        result = webp('path/to/the/image.png')
        self.assertEqual(self.expected, result)

    def test_templatetag_in_template(self):
        rendered = self.render_template('{% load webp %}{% webp "path/to/the/image.png" %}')
        self.assertEqual(self.expected, rendered)


class ViewIndexTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('django_webp', args=('django_webp/python.png', ))

    def test_simple_request(self):
        """ should return an image converted to webp """
        image = _get_converted_image()

        for user_agent in USER_AGENTS:
            headers = { 'HTTP_USER_AGENT': user_agent }
            response = self.client.get(self.url, **headers)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get('Content-Type'), 'image/webp')

            self.assertTrue(image == response.content, 'Image was not webp')

    def test_404(self):
        """ Should raise a 404 """
        url = reverse('django_webp', args=('django_webp/not-exist.png', ))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)



class MiddlewareWebpTest(unittest.TestCase):

    def setUp(self):
        pass

    #def process_request(self, request):
    #def process_response(self, request, response):
