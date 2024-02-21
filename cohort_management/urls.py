from django.urls import path
from .views import (
    CohortListAPIView,
    CohortCreateAPIView,
    CohortRetrieveUpdateDestroyAPIView,
    InternProfileListAPIView,
    InternProfileCreateAPIView,
    InternProfileRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # Cohort URLs
    path('cohorts/', CohortListAPIView.as_view(), name='cohort-list'),
    path('cohorts/create/', CohortCreateAPIView.as_view(), name='cohort-create'),
    path('cohorts/<int:pk>/', CohortRetrieveUpdateDestroyAPIView.as_view(), name='cohort-detail'),

    # Intern Profile URLs
    path('intern-profiles/', InternProfileListAPIView.as_view(), name='intern-profile-list'),
    path('intern-profiles/create/', InternProfileCreateAPIView.as_view(), name='intern-profile-create'),
    path('intern-profiles/<int:pk>/', InternProfileRetrieveUpdateDestroyAPIView.as_view(), name='intern-profile-detail'),
]
