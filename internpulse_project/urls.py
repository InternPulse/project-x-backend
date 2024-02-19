"""
URL configuration for internpulse_project project.
Each module or app will have their own URL configuration, and the main project will have a URL configuration that references the URL configuration of each app.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Internpulse",
        default_version='v1',
        description="API documentation for Internpulse",

    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
     path('admin/', admin.site.urls),
     path('auth/', include('user_management.urls')),
     path('cohort/', include('cohort_management.urls')),  # Include cohort_management URLs
     path('interns/', include('cohort_management.urls')),  # Include cohort_management URLs
     path('api/', include('cohort_management.urls')),  # Include cohort management URLs
]
