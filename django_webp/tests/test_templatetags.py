import unittest
import os
import shutil

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.files.storage import FileSystemStorage
from django.template import Template, Context
from django.test.utils import override_settings
from django.templatetags.static import static

from django_webp.templatetags.webp import webp
from django_webp.utils import WEBP_STATIC_URL, WEBP_STATIC_ROOT


class TemplateTagTest(unittest.TestCase):

    def setUp(self):
        self.supported_url = WEBP_STATIC_URL + 'django_webp/python.webp'
        self.unsupported_url = static('django_webp/python.png')

    def tearDown(self):
        # cleaning the folder the files here
        try:
            shutil.rmtree(WEBP_STATIC_ROOT)
        except:
            pass

    def _assertFile(self, file_path, msg=''):
        STATIC_ROOT = settings.STATIC_ROOT if settings.STATIC_ROOT.endswith('/') else settings.STATIC_ROOT + '/'
        staticfile_path = file_path.replace(settings.STATIC_URL, settings.STATIC_ROOT)
        file_exist = os.path.isfile(staticfile_path)

        msg = msg or ('file doesnt exist: %s' % staticfile_path)
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


    def test_supports_webp_false(self):
        context = self._get_invalid_context()
        result = webp(context, 'django_webp/python.png')
        expected = static('django_webp/python.png')
        self.assertEqual(result, expected)


    def test_templatetag(self):
        """ checks the returned url from the webp function """
        context = self._get_valid_context()
        result = webp(context, 'django_webp/python.png')
        self.assertEqual(self.supported_url, result)
        self._assertFile(result, 'file %s should have been created' % result)


    def test_templatetag_in_template(self):
        html = '{% load webp %}{% webp "django_webp/python.png" %}'
        rendered = self._render_template(html, context=self._get_valid_context())
        self.assertEqual(self.supported_url, rendered)
        self._assertFile(rendered, 'file %s should have been created' % rendered)


    def test_debug_true(self):
        """ if DEBUG = True, should always return the static url """
        context = self._get_valid_context()
        result = webp(context, 'django_webp/python.png', force_static=True)
        self.assertEqual(self.unsupported_url, result)
