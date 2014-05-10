# -*- coding: utf-8 -*-
import unittest
import os

from django.template import Template, Context
from django.contrib.staticfiles.templatetags.staticfiles import static

from django_webp.templatetags.webp import webp
from django_webp.utils import WEBP_STATIC_URL


class TemplateTagTest(unittest.TestCase):

    def setUp(self):
        self.supported_url = WEBP_STATIC_URL + 'django_webp/python.png'
        self.unsupported_url = static('django_webp/python.png')
        self.context = Context({})


    def tearDown(self):
        # clean the files here
        pass


    def _assertFile(self, file_path, msg=''):
        file_exist = os.path.isfile(file_path)
        self.assertTrue(file_exist, msg)


    def _get_valid_context(self):
        return Context({'supports_webp': True})


    def _get_invalid_context(self):
        return Context({'supports_webp': False})


    def _render_template(self, html, context={}):
        return Template(html).render(Context(context))


    def test_unexistent_image(self):
        """ If the given image doesn't exist, return the static url """
        context = self._get_valid_context()
        result = webp(context, 'django_webp/this_image_doesnt_exist.gif')
        expected = static('django_webp/this_image_doesnt_exist.gif')
        self.assertEqual(result, expected)


    def test_templatetag(self):
        """ checks the returned url from the webp function """
        context = self._get_valid_context()
        result = webp(context, 'django_webp/python.png')
        self.assertEqual(self.supported_url, result)
        self._assertFile(result, 'file should have been created')


    def test_templatetag_in_template(self):
        html = '{% load webp %}{% webp "django_webp/python.png" %}'
        rendered = self._render_template(html, context=self._get_valid_context())
        self.assertEqual(self.supported_url, rendered)
        self._assertFile(rendered, 'file should have been created')
