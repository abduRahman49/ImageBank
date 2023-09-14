import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from image_bank import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from allauth.account.views import SignupView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/contributeur/singup/', views.signup_contributeur, name='sign-up-contributeur'),
    path('accounts/contributeur/signin/', views.signin_contributeur, name='sign-in-contributeur'),
    path('accounts/logout/', views.logout_view, name='sign-out'),
    # path('users/signup', SignupView.as_view(), name='sign-up'),
    path('contributeur/index/', views.index_contributeur, name='index-contributeur'),
    path('contributeur/images/', views.images_contributeur, name='images-contributeur'),
    path('contributeur/images/<int:id>/', views.detail_image, name='detail-image'),
    path('contributeur/accueil/', views.accueil_images, name='accueil-images'),
    path('contributeur/images/upload/', views.upload_image, name="upload-contributeur"),
    path('api/v1/edit/images/<int:id>/', views.update_image, name="edit-image"),
    path('api/v1/delete/images/<int:id>/', views.delete_image, name="delete-image"),
    path('contributeur/images/search/', views.search_images, name="recherche-images"),
    path('api/v1/images/<int:id>/json/', views.get_json_image),
    path('api/', include('api.urls')),
    path("__debug__/", include(debug_toolbar.urls)),
    path('accounts/', include('allauth.urls')),
    path('', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
