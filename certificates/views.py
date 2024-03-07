from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.response import Response

from .models import Certificate
from .serializers import CertificateSerializer, CertificateIssueBatchSerializer, CertificateDetailSerializer

from cohort_management.models import InternProfile, Cohort


class CertificateCreateAPIView(generics.CreateAPIView):
    """
    A view to create a certificate.
    """
    serializer_class = CertificateSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        """
        Create a new certificate.

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
                "message": "Certificate created successfully",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
class CertificateListAPIView(generics.ListAPIView):
    """
    A view to list all certificates.
    """
    serializer_class = CertificateDetailSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Certificate.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Get a list of all certificates.

        Returns:
            Response: RESTful response with a list of certificates.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True)
        data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Certificates retrieved successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class CertificateDetailAPIView(generics.RetrieveAPIView):
    """
    A view to retrieve a cohort.

    Allows unauthenticated and authenticated users to retrieve a certificate by its ID.
    """
    queryset = Certificate.objects.all()
    serializer_class = CertificateDetailSerializer
    parser_classes = [MultiPartParser, FormParser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific certificate.

        Args:
            request: The request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: RESTful response with the retrieved certificate.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Certificate retrieved successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class CertificateUpdateAPIView(generics.UpdateAPIView):
    """
    A view to update a certificate.

    Allows only authenticated users to update a certificate by its ID.
    """
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        """
        Update a specific certificate.

        Args:
            request: The request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: RESTful response indicating the result of the update operation.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Certificates updated successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class CertificateDestroyAPIView(generics.DestroyAPIView):
    """
    A view to delete a certificate.

    Allows only authenticated users to delete a cohort by its ID.
    """
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific certificate.

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
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Certificate deleted successfully"
        }
        return Response(data, status=status.HTTP_200_OK)


class CertificateIssueBatchAPIView(generics.CreateAPIView):
    """
    A view to issue certificates in batch.

    Allows only authenticated admin users to issue certificates to users by their IDs or cohort ID.
    """
    serializer_class = CertificateIssueBatchSerializer
    permission_classes = [IsAdminUser]  # Authentication required

    def post(self, request):
        """
        Issue certificates in batch to users.

        Args:
            request: The request object.

        Returns:
            Response: RESTful response indicating the result of the issued operation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        intern_ids = serializer.validated_data.get('intern_profile_ids', [])
        cohort_id = serializer.validated_data.get('cohort_id')

        if not intern_ids and not cohort_id:
            data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Please provide intern_ids or cohort_id"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if cohort_id:
            try:
                cohort = Cohort.objects.get(id=cohort_id)
            except Cohort.DoesNotExist:
                data = {
                    "status": status.HTTP_204_NO_CONTENT,
                    "success": False,
                    "message": "Cohort does not exist"
                }
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            interns = InternProfile.objects.filter(cohort=cohort)
        else:
            interns = InternProfile.objects.filter(id__in=intern_ids)

        certificates_issued = []
        for intern in interns:
            certificate = Certificate(user=intern.user, cohort=intern.cohort, is_issued=True)
            certificate.save()
            certificates_issued.append({'intern_id': intern.id, 'certificate_id': certificate.id})

        data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Certificate issued successfully",
            "certificates_issued": certificates_issued
        }
        return Response(data, status=status.HTTP_200_OK)
