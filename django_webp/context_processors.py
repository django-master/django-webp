from django.conf import settings


WEBP_VALID_BROWSERS = getattr(settings, 'WEBP_VALID_BROWSERS', ['Chrome', 'Opera', 'Opera Mobile'])


def webp(request):
    """ Adds `supports_webp` value in the context """

    return {'supports_webp': False}
