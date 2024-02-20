from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Cohort, InternProfile
from .serializers import CohortSerializer, InternProfileSerializer

class CohortListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cohort.objects.all()

    def get(self, request, *args, **kwargs):
        cohorts = self.get_queryset()
        serializer = self.serializer_class(cohorts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CohortRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated]

class InternProfileListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = InternProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InternProfile.objects.order_by('created_at')

    def get(self, request, *args, **kwargs):
        profiles = self.get_queryset()
        serializer = self.serializer_class(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InternProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InternProfile.objects.all()
    serializer_class = InternProfileSerializer
    permission_classes = [IsAuthenticated]
