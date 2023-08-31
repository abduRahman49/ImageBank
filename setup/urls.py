import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from image_bank import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('api/v1/upload/images/', views.upload_image),
    path('api/v1/edit/images/<int:id>/', views.update_image),
    path('api/v1/images/<int:id>/json/', views.get_json_image),
    path('api/', include('api.urls')),
    path("__debug__/", include(debug_toolbar.urls)),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
