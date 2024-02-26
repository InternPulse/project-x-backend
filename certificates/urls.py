from django.urls import path
from .views import CertificateListCreateAPIView, CertificateDetailAPIView, CertificateIssueBatchAPIView


urlpatterns = [
    path("certificates/", CertificateListCreateAPIView.as_view(), name="certificate-list-create"),
    path("certificates/<int:pk>/", CertificateDetailAPIView.as_view(), name="certificate-detail"),
    path(
        "certificates/issue-batch/",
        CertificateIssueBatchAPIView.as_view(),
        name="certificate-issue-batch",
    ),
]
