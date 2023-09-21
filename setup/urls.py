import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from image_bank import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/contributeur/singup/', views.signup_contributeur, name='sign-up-contributeur'),
    path('accounts/contributeur/signin/', views.signin_contributeur, name='sign-in-contributeur'),
    path('accounts/user/signup/', views.signup_user, name='sign-up-user'),
    path('accounts/user/signin/', views.signin_user, name='sign-in-user'),
    path('logout/', views.logout_view, name='sign-out'),
    path('contributeur/index/', views.index_contributeur, name='index-contributeur'),
    path('user/index/', views.user_index, name='user-index'),
    path('contributeur/images/', views.images_contributeur, name='images-contributeur'),
    path('user/images/<int:id>/', views.detail_image, name='detail-image'),
    path('contributeur/accueil/', views.accueil_images, name='accueil-images'),
    path('contributeur/images/upload/', views.upload_image, name="upload-contributeur"),
    path('api/v1/edit/images/<int:id>/', views.update_image, name="edit-image"),
    path('api/v1/delete/images/<int:id>/', views.delete_image, name="delete-image"),
    path('contributeur/images/search/<int:id>/', views.search_images, name="recherche-images"),
    path('user/images/search/', views.search_images, name="recherche-images"),
    path('profil/', views.profil, name='profil'),
    path('profile/password/edit/', views.edit_password, name='edit-password'),
    path('profile/picture/edit/', views.edit_profile, name='edit-profile'),
    path('password/check/', views.check_password, name='check-password'),
    path('password/reset/', views.reset_password, name='reset-password'),
    path('picture/edit', views.edit_picture, name='edit-picture'),
    path('api/v1/images/<int:id>/json/', views.get_json_image),
    path('api/v1/images/<int:id>/download/', views.download_image, name='image-download'),
    path('api/', include('api.urls')),
    # path("__debug__/", include(debug_toolbar.urls)),
    # path('accounts/', include('allauth.urls')),
    path('login/', views.login_users, name='login-users'),
    path('', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
