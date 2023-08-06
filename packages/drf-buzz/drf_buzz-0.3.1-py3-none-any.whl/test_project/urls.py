from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from rest_framework import routers

from .test_app.views import TestViewSet


router = routers.SimpleRouter()
router.register(r"test", TestViewSet, basename="test")

urlpatterns = [url(r"^", include(router.urls))]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
