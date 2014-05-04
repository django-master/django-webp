# -*- coding: utf-8 -*-
import unittest

from django.template import Template, Context

from django_webp.templatetags.webp import webp, WEBP_URL


class TemplateTagTest(unittest.TestCase):

    def setUp(self):
        self.expected = '%s/path/to/the/image.png' % (WEBP_URL, )

    def render_template(self, html, context={}):
        return Template(html).render(Context(context))

    def test_templatetag(self):
        result = webp('path/to/the/image.png')
        self.assertEqual(self.expected, result)

    def test_templatetag_in_template(self):
        rendered = self.render_template('{% load webp %}{% webp "path/to/the/image.png" %}')
        self.assertEqual(self.expected, rendered)


class MiddlewareWebpTest(unittest.TestCase):

    def setUp(self):
        pass

    #def process_request(self, request):
    #def process_response(self, request, response):
