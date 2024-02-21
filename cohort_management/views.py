from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cohort, InternProfile
from .serializers import CohortSerializer, InternProfileSerializer

class CohortListAPIView(generics.ListAPIView):
    """
    A view to list all cohorts.

    Retrieves all cohorts from the database and serializes them using the CohortSerializer.
    """
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated]

class CohortCreateAPIView(generics.CreateAPIView):
    """
    A view to create a new cohort.

    Allows authenticated users to create a new cohort by providing the necessary data in the request body.
    """
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CohortRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view to retrieve, update, or delete a cohort.

    Allows authenticated users to retrieve, update, or delete a cohort by its ID.
    """
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated]

class InternProfileListAPIView(generics.ListAPIView):
    """
    A view to list all intern profiles.

    Retrieves all intern profiles from the database and serializes them using the InternProfileSerializer.
    """
    queryset = InternProfile.objects.all()
    serializer_class = InternProfileSerializer
    permission_classes = [IsAuthenticated]

class InternProfileCreateAPIView(generics.CreateAPIView):
    """
    A view to create a new intern profile.

    Allows authenticated users to create a new intern profile by providing the necessary data in the request body.
    """
    serializer_class = InternProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InternProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view to retrieve, update, or delete an intern profile.

    Allows authenticated users to retrieve, update, or delete an intern profile by its ID.
    """
    queryset = InternProfile.objects.all()
    serializer_class = InternProfileSerializer
    permission_classes = [IsAuthenticated]
