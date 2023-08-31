from django.urls import path
from rest_framework import routers
from .views import ImageModelViewset, LicenceModelViewset, ImageSearchAPIView

router = routers.SimpleRouter()
router.register(r'images', ImageModelViewset)
router.register(r'licences', LicenceModelViewset)

urlpatterns = [
    path('images/search/', ImageSearchAPIView.as_view())
]

urlpatterns += router.urls
