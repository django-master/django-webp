import os

from django.test import TestCase
from django.conf import settings

from django_webp.templatetags.webp import WEBPImageConverter


class WEBPImageConverterTestCase(TestCase):

    def test_generate_webp_image_when_file_doesnt_exist(self):
        image_path = os.path.join(settings.BASE_DIR, 'testapp', 'static', 'django_webp', 'does-not-exist.png')
        generated_path = os.path.join(settings.BASE_DIR, 'staticfiles', 'python.webp')

        converter = WEBPImageConverter()
        self.assertFalse(converter.generate_webp_image(generated_path, image_path))