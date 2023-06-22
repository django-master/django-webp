# -*- coding: utf-8 -*-
import os
import unittest
from PIL import Image

from django.test.client import Client
from django.contrib.staticfiles import finders
from django.core.management import call_command
from django.core.management.base import CommandError

from django_webp.utils import WEBP_STATIC_ROOT


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


class MainTest(unittest.TestCase):

    def test_pillow(self):
        """ Checks if current pillow installation
        has support to WEBP """
        image = Image.open(IMAGE_PNG_PATH)
        try:
            image.load()
            self.assertTrue(True)
        except:
            self.assertFail("There is no support for webp")


    def test_index(self):
        client = Client()
        response = client.get('/')

        self.assertEqual(response.status_code, 200)


    def test_clean_webp_images_command(self):
        call_command('collectstatic', '--noinput', '--clear')
        self.assertRaises(CommandError, call_command, 'clean_webp_images')
