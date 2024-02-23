from django.urls import path
from .views import CertificateListCreateAPIView, CertificateDetailAPIView, CertificateIssueBatchAPIView


#app_name = "certificates"

urlpatterns = [
    path("", CertificateListCreateAPIView.as_view(), name="certificate-list-create"),
    path("<int:pk>/", CertificateDetailAPIView.as_view(), name="certificate-detail"),
    path(
        "issue-batch/",
        CertificateIssueBatchAPIView.as_view(),
        name="certificate-issue-batch",
    ),
]
