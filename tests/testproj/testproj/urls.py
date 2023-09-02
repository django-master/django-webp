from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Only for test purposes

urlpatterns = [
    path('', include('testapp.urls')),
]