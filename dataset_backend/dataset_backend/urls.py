from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular import views as drf_views

urlpatterns = [
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
        'api/schema/',
        drf_views.SpectacularAPIView.as_view(),
        name='schema'
        ),
    path(
        'api/rest/',
        include('rest_framework.urls'),
        name='rest_framework'
    ),
    path('api/v1/slides/', include('slides.api.urls')),
    path('api/v1/datasources/', include('datasources.api.urls')),
    path('connections/api/', include('connections.api.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
