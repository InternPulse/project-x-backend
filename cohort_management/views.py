from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user_management.permissions import IsAdminPermission 
from .models import Cohort, InternProfile
from .serializers import CohortSerializer, InternProfileSerializer

class CohortListAPIView(generics.ListAPIView):
    """
    A view to list all cohorts.

    Retrieves all cohorts from the database and serializes them using the CohortSerializer.
    """
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated, IsAdminPermission]

    def list(self, request, *args, **kwargs):
        """
        Get a list of all cohorts.

        Returns:
            Response: RESTful response with a list of cohorts.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "status": 200,
            "success": True,
            "message": "Cohorts retrieved successfully",
            "data": serializer.data
        }
        return Response(data)

class CohortCreateAPIView(generics.CreateAPIView):
    """
    A view to create a new cohort.

    Allows only admin users to create a new cohort by providing the necessary data in the request body.
    """
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated, IsAdminPermission]

    def post(self, request, *args, **kwargs):
        """
        Create a new cohort.

        Args:
            request: The request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: RESTful response indicating the result of the create operation.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Cohort created successfully",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CohortRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view to retrieve, update, or delete a cohort.

    Allows authenticated users to retrieve, update, or delete a cohort by its ID.
    """
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated, IsAdminPermission]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific cohort.

        Args:
            request: The request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: RESTful response with the retrieved cohort.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Cohort retrieved successfully",
            "data": serializer.data
        }
        return Response(data)

    def update(self, request, *args, **kwargs):
        """
        Update a specific cohort.

        Args:
            request: The request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: RESTful response indicating the result of the update operation.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Cohort updated successfully",
            "data": serializer.data
        }
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific cohort.

        Args:
            request: The request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: RESTful response indicating the result of the delete operation.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {
            "status": status.HTTP_204_NO_CONTENT,
            "success": True,
            "message": "Cohort deleted successfully"
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

class InternProfileListAPIView(generics.ListAPIView):
    """
    A view to list all intern profiles.

    Retrieves all intern profiles from the database and serializes them using the InternProfileSerializer.
    """
    queryset = InternProfile.objects.all()
    serializer_class = InternProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminPermission]  # Restrict access to admin users only

    def list(self, request, *args, **kwargs):
        """
        Get a list of all intern profiles.

        Returns:
            Response: RESTful response with a list of intern profiles.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "status": 200,
            "success": True,
            "message": "Intern profiles retrieved successfully",
            "data": serializer.data
        }
        return Response(data)

class InternProfileCreateAPIView(generics.CreateAPIView):
    """
    A view to create a new intern profile.

    Allows authenticated users to create a new intern profile by providing the necessary data in the request body.
    """
    serializer_class = InternProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Create a new intern profile.

        Args:
            request: The request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: RESTful response indicating the result of the create operation.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Intern profile created successfully",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InternProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view to retrieve, update, or delete an intern profile.

    Allows authenticated users to retrieve, update, or delete an intern profile by its ID.
    """
    queryset = InternProfile.objects.all()
    serializer_class = InternProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminPermission]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific intern profile.

        Args:
            request: The request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: RESTful response with the retrieved intern profile.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Intern profile retrieved successfully",
            "data": serializer.data
        }
        return Response(data)

    def update(self, request, *args, **kwargs):
        """
        Update a specific intern profile.

        Args:
            request: The request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: RESTful response indicating the result of the update operation.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Intern profile updated successfully",
            "data": serializer.data
        }
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific intern profile.

        Args:
            request: The request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: RESTful response indicating the result of the delete operation.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {
            "status": status.HTTP_204_NO_CONTENT,
            "success": True,
            "message": "Intern profile deleted successfully"
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
