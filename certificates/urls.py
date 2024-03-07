from django.urls import path
from . import views


urlpatterns = [
    path("certificates/", views.CertificateListAPIView.as_view(), name="certificate-list"),
    path("certificate/create/", views.CertificateCreateAPIView.as_view(), name="certificate-create"),
    path("certificate/detail/<int:pk>/", views.CertificateDetailAPIView.as_view(), name="certificate-detail"),
    path("certificate/update/<int:pk>/", views.CertificateUpdateAPIView.as_view(), name="certificate-update"),
    path("certificate/delete/<int:pk>/", views.CertificateDestroyAPIView.as_view(), name="certificate-destroy"),
    path(
        "certificates/issue-batch/",
        views.CertificateIssueBatchAPIView.as_view(),
        name="certificate-issue-batch",
    ),
]
