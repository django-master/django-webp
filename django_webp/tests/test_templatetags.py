# -*- coding: utf-8 -*-
import unittest

from django.template import Template, Context
from django.core.urlresolvers import reverse

from django_webp.templatetags.webp import webp


class TemplateTagTest(unittest.TestCase):

    def setUp(self):
        self.expected = reverse('django_webp', args=('path/to/the/image.png', ))
        self.context = Context({})


    def _get_valid_context(self):
        return Context({'supports_webp': True})


    def _get_invalid_context(self):
        return Context({'supports_webp': False})


    def render_template(self, html, context={}):
        return Template(html).render(Context(context))


    def test_templatetag(self):
        context = self._get_valid_context()
        result = webp(context, 'path/to/the/image.png')
        self.assertEqual(self.expected, result)


    def test_templatetag_in_template(self):
        rendered = self.render_template('{% load webp %}{% webp "path/to/the/image.png" %}')
        self.assertEqual(self.expected, rendered)
