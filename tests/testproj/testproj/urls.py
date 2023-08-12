from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


# Only for test purposes

urlpatterns = [
    path('', include('testapp.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)