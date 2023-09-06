from django.urls import path
from rest_framework import routers
from .views import ImageModelViewset, LicenceModelViewset, ImageSearchAPIView, AuteurModelViewset

router = routers.SimpleRouter()
router.register(r'images', ImageModelViewset)
router.register(r'licences', LicenceModelViewset)
router.register(r'auteurs', AuteurModelViewset)

urlpatterns = [
    path('images/search/', ImageSearchAPIView.as_view())
]

urlpatterns += router.urls
