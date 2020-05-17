import unittest

from django.http import HttpRequest

from django_webp.tests.test_main import USER_AGENTS
from django_webp.context_processors import webp


class ContextProcessorTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()


    def test_common_return(self):
        """ Must return False in the dic """
        result = webp(self.request)
        supports_webp = result.get('supports_webp', None)
        self.assertFalse(supports_webp)


    def test_by_user_agent(self):
        """ Giving a valid user agent, should return True """
        self.request.META['HTTP_USER_AGENT'] = USER_AGENTS[0]
        result = webp(self.request)
        supports_webp = result.get('supports_webp', None)
        self.assertTrue(supports_webp)


    def test_by_http_accept_header(self):
        """
        Giving a valid http accept header, shold return True
        @see -> https://www.igvita.com/2013/05/01/deploying-webp-via-accept-content-negotiation/
        """
        self.request.META['HTTP_ACCEPT'] = 'image/webp'
        result = webp(self.request)
        supports_webp = result.get('supports_webp', None)
        self.assertTrue(supports_webp)