# -*- coding: utf-8 -*-


def _check_by_http_accept_header(http_accept):
    return "webp" in http_accept


def webp(request):
    """Adds `supports_webp` value in the context"""
    http_accept = request.META.get("HTTP_ACCEPT", "")

    if _check_by_http_accept_header(http_accept):
        supports_webp = True
    else:
        supports_webp = False

    return {"supports_webp": supports_webp}
