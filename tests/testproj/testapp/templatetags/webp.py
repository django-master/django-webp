# -*- coding: utf-8 -*-
import os
import logging
import requests
from io import BytesIO
from PIL import Image

from django import template
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.staticfiles import finders
from django.core.files.storage import default_storage
from django.templatetags.static import static
from django.core.exceptions import SuspiciousFileOperation

from whitenoise.middleware import WhiteNoiseMiddleware
from whitenoise.string_utils import ensure_leading_trailing_slash

from django.conf import settings
from utils import (
    WEBP_STATIC_ROOT,
    WEBP_DEBUG,
    WEBP_CHECK_URLS,
)

# if STATIC_ROOT is abs, then we are likely woring in production, if not, likely a testing env
if os.path.isabs(settings.STATIC_ROOT):
    base_path = settings.STATIC_ROOT
    static_dir_prefix = os.path.relpath(settings.STATIC_ROOT, start=settings.BASE_DIR)
else:
    base_path = os.path.join(settings.BASE_DIR, settings.STATIC_ROOT)
    static_dir_prefix = settings.STATIC_ROOT

# getting rid of trailing slash
static_dir_prefix = (static_dir_prefix).rstrip("/")

register = template.Library()


class WEBPImageConverter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_path(self, image_path):
        """creates all folders necessary until reach the file's folder"""
        folder_path = os.path.dirname(image_path)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

    def get_static_image(self, image_url):
        if "https://" in image_url:
            return image_url
        else:
            return static(image_url)
        
    def check_image_dirs(self, generated_path, image_path):
        """
        Checks if original image directory is valid and prevents duplicates of 
        generated images by checking if the already exist in a directory
        """

        # Checking if original image exists
        if not os.path.exists(os.path.join(base_path, image_path)) and not "https" in image_path:
            self.logger.warn(f"Original image does not exist in static files path: {os.path.join(base_path, image_path)}")
            return False
        
        # Checks if the webp version of the image exists
        if os.path.exists(generated_path):
            return False
        else:
            return True
        
    def is_image_served(self, image_url, timeout_seconds=1):
        try:
            response = requests.head(image_url, timeout=timeout_seconds)
            if response.status_code == requests.codes.ok:
                return True
            else:
                return False
        except requests.exceptions.Timeout:
            return False
        except requests.exceptions.RequestException as e:
            return False

    def get_generated_image(self, image_url):
        """Returns the url to the webp gerenated image, returns the
        original image url if any of the following occur:
        
        - webp image generation fails
        - original image does not exist
        """

        if "https://" in image_url:  # pragma: no cover
            # Split the text by forward slashes and gets the last part (characters after the last slash)
            raw_filename = image_url.split("/")[-1]
            real_url = os.path.join(
                "online_images/", os.path.splitext(raw_filename)[0] + ".webp"
            )
        else:
            real_url = os.path.splitext(image_url)[0] + ".webp"

        generated_path = os.path.join(WEBP_STATIC_ROOT, real_url).lstrip("/")
        
        # Checks if link provided is still valid
        # Only bothers to check if the link is valid if WEBP_CHECK_URLS is True
        if "https://" in image_url: # pragma: no cover
            if WEBP_CHECK_URLS:
                try:
                    response = requests.head(image_url)
                    if response.status_code == requests.codes.ok:
                        content_type = response.headers.get("Content-Type", "")
                        if not content_type.startswith("image/"):
                            self.logger.warn(f"The following image url is invalid: {image_url}")
                except requests.RequestException:
                    return self.get_static_image(image_url)
        
        should_generate = self.check_image_dirs(generated_path, image_url)
        
        if should_generate is True:
            if "https://" in image_url: # pragma: no cover
                if not self.generate_webp_image(generated_path, image_url):
                    self.logger.error(f"Failed to generate from URL: {image_url}")
                    return self.get_static_image(image_url)
            else:
                # Constructing full image path for original image
                image_path = os.path.join(base_path, image_url)
                if not self.generate_webp_image(generated_path, image_path):
                    return self.get_static_image(image_url)
        
        ## converting generated_path from an absolute path to a relative path
        index = generated_path.find(static_dir_prefix)
        # Extract the substring starting from static_dir_prefix and replacing any weird backslashes with forward slashes
        generated_path = (generated_path[index + len(static_dir_prefix):]).replace("\\", "/")

        
        # have to check if image is served bc webp runs before whitenoise can properly hash the image dirs
        domain = os.environ.get("HOST", default="http://127.0.0.1:8000/")
        if self.is_image_served(domain.rstrip("/") + static(generated_path)):
            return static(generated_path)
        else:
            return self.get_static_image(image_url)

    def generate_webp_image(self, generated_path, image_path):
        final_path = os.path.join(str(base_path), generated_path)

        ## Generating images if they do not exist in a directory
        # Fetching the image data
        if "https://" in image_path: # pragma: no cover
            response = requests.get(image_path)
            try:
                image = Image.open(BytesIO(response.content))
            except:
                self.logger.error(f"Error: Failed to read the image file from URL: {image_path}")
                return False
        else:
            try:
                image = Image.open(image_path)
            except FileNotFoundError:
                return False

        # Using the image data to save a webp version of it to static files
        try:
            self.generate_path(generated_path)
            # we use a buffer to store the contents of our conversion before saving to disk
            buffer = BytesIO()
            image.save(buffer, "WEBP")
            content_file = ContentFile(buffer.getvalue())
            default_storage.save(final_path, content_file)
            image.close()
            return True
        except KeyError: # pragma: no cover
            self.logger.error("WEBP is not installed in Pillow")
        except (IOError, OSError): # pragma: no cover
            self.logger.error("WEBP image could not be saved in %s" % generated_path)
        except SuspiciousFileOperation:
            self.logger.error("SuspiciousFileOperation: the generated image was created outside of the base project path %s" % generated_path)

        return False  # pragma: no cover


@register.simple_tag(takes_context=True)
def webp(context, value, force_static=WEBP_DEBUG):
    converter = WEBPImageConverter()

    supports_webp = context.get("supports_webp", False)
    if not supports_webp or not force_static:
        return converter.get_static_image(value)

    return converter.get_generated_image(value)
