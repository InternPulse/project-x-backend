"""
URL configuration for internpulse_project project.
Each module or app will have their own URL configuration, and the main project will have a URL configuration that references the URL configuration of each app.
"""
from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Invoice Pilot API",
        default_version='v1',
        description="API documentation for Invoice Pilot",
        url="https://psychic-meme-5j5657xvpw5297q-8000.app.github.dev/"


    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
     path('admin/', admin.site.urls),
]
