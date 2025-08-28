from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular import views as drf_views
from rest_framework_simplejwt import views as auth_views

urlpatterns = [
    path(
        'api/schema/',
        drf_views.SpectacularAPIView.as_view(),
        name='schema'
    ),
    path(
        'api/schema/swagger-ui/',
        drf_views.SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/schema/redoc/',
        drf_views.SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
    path(
        'v1/auth/token/',
        auth_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/auth/token/refresh/',
        auth_views.TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'v1/documents/',
        include('tabledocuments.urls')
    ),
    path(
        'v1/tables/',
        include('dbtables.urls')
    ),
    path(
        'v1/databases/',
        include('dbschemas.urls')
    ),
    path(
        'admin/',
        admin.site.urls
    )
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
