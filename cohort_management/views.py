# cohort_management/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Cohort, InternProfile
from .serializers import CohortSerializer, InternProfileSerializer

class CohortListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated]

class CohortRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated]

class InternProfileListCreateAPIView(generics.ListCreateAPIView):
    queryset = InternProfile.objects.order_by('created_at')
    serializer_class = InternProfileSerializer
    permission_classes = [IsAuthenticated]

class InternProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InternProfile.objects.all()
    serializer_class = InternProfileSerializer
    permission_classes = [IsAuthenticated]
