# -*- coding: utf-8 -*-
import os
import unittest
from PIL import Image

from django.test.client import Client
from django.contrib.staticfiles import finders
from django.core.management import call_command
from django.core.management.base import CommandError


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
