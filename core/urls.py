from django.urls import path, include

urlpatterns = [
    path('/cms/', include('cms.urls'))
]
