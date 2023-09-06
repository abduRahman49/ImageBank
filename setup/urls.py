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
    path('accounts/singup/', views.signup, name='sign-up'),
    path('accounts/signin/', views.signin, name='sign-in'),
    path('accounts/logout/', views.logout_view, name='sign-out'),
    # path('users/signup', SignupView.as_view(), name='sign-up'),
    path('api/v1/upload/images/', views.upload_image),
    path('api/v1/edit/images/<int:id>/', views.update_image),
    path('api/v1/images/<int:id>/json/', views.get_json_image),
    path('api/', include('api.urls')),
    path("__debug__/", include(debug_toolbar.urls)),
    path('accounts/', include('allauth.urls')),
    path('home/', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
