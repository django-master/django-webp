# -*- coding: utf-8 -*-
import unittest

from django.test.client import Client
from django.core.urlresolvers import reverse

from .main import USER_AGENTS


class ViewIndexTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('django_webp', args=('django_webp/python.png', ))

    def test_simple_request(self):
        """ should return an image converted to webp """
        for user_agent in USER_AGENTS:
            headers = { 'HTTP_USER_AGENT': user_agent }
            response = self.client.get(self.url, **headers)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get('Content-Type'), 'image/webp')

    def test_404(self):
        """ Should raise a 404 """
        url = reverse('django_webp', args=('django_webp/not-exist.png', ))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

