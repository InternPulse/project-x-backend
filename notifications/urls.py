from django.urls import path
from .views import TalentRequestTicketRegistrationView

urlpatterns = [
    path(
        "talent-request",
        TalentRequestTicketRegistrationView.as_view(),
        name="talent-request",
    ),
]
