from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from testapp.views import index


# Only for test purposes

urlpatterns = [
    path('', index),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
