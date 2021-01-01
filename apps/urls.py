from django.urls import path, include

from .cms import urls

urlpatterns = [path("cms/", include("apps.cms.urls"))]
