from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from user_management.views import UserRedirectView

schema_view = get_schema_view(
    openapi.Info(
        title="Internpulse",
        default_version="v1",
        description="API documentation for Internpulse",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path("~redirect/", UserRedirectView.as_view(), name="redirect"),
    # path("api/v1/", include('allauth.urls')), # We're not using the google login so disabled for now
    path('api/v1/', include('user_management.urls')),
    path('api/v1/', include('cohort_management.urls')),  # Include cohort_management URLs
    path('api/v1/', include('cohort_management.urls')),  # Include cohort_management URLs
    path('api/v1/', include('cohort_management.urls')),  # Include cohort management URLs
    path('api/v1/', include('certificates.urls')),  # Include certificate URLs
    path('api/v1/payment/', include('paymentintergration.urls')),  # Adjusted URL for payment integration
    path('api/v1/user/', include('user_management.urls')),  # Adjusted URL for user management
    path('api/v1/cohort/', include('cohort_management.urls')),  # Adjusted URL for cohort management
    path('api/v1/certificates/', include('certificates.urls')),  # Adjusted URL for certificates

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
