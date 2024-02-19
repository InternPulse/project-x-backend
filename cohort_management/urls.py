# cohort_management/urls.py
from django.urls import path
from .views import (
    CohortListCreateAPIView,
    CohortRetrieveUpdateDestroyAPIView,
    InternProfileListCreateAPIView,
    InternProfileRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # Cohort URLs
    path('cohorts/', CohortListCreateAPIView.as_view(), name='cohort-list-create'),
    path('cohorts/<int:pk>/', CohortRetrieveUpdateDestroyAPIView.as_view(), name='cohort-detail'),

    # Intern Profile URLs
    path('intern-profiles/', InternProfileListCreateAPIView.as_view(), name='intern-profile-list-create'),
    path('intern-profiles/<int:pk>/', InternProfileRetrieveUpdateDestroyAPIView.as_view(), name='intern-profile-detail'),
]
