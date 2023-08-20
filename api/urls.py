from django.urls import path
from rest_framework import routers
from .views import ImageModelViewset, LicenceModelViewset

router = routers.SimpleRouter()
router.register(r'images', ImageModelViewset)
router.register(r'licences', LicenceModelViewset)

urlpatterns = [
    
]

urlpatterns += router.urls
