# -*- coding: utf-8 -*-
import unittest

from django_webp.templatetags.webp import webp, WEBP_URL


class TemplateTagTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_templatetag(self):
        expected = '%s/path/to/the/image.png' % (WEBP_URL, )
        result = webp('path/to/the/image.png')

        self.assertEqual(expected, result)



class MiddlewareWebpTest(unittest.TestCase):

    def setUp(self):
        pass

    #def process_request(self, request):
    #def process_response(self, request, response):
