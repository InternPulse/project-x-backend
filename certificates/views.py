from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from django.http import Http404

from .models import Certificate
from .serializers import CertificateSerializer, CertificateIssueBatchSerializer

from cohort_management.models import InternProfile, Cohort


# Create your views here.
class CertificateListCreateAPIView(generics.ListCreateAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


class CertificateDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateIssueBatchSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


class CertificateIssueBatchAPIView(generics.CreateAPIView):
    serializer_class = CertificateIssueBatchSerializer
    permission_classes = [IsAuthenticated]  # Authentication required
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        context = {}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        intern_ids = serializer.validated_data.get('intern_ids')
        cohort_id = serializer.validated_data.get('cohort_id')
        certificate_id = serializer.validated_data.get('certificate_id')

        if not intern_ids and not cohort_id and not certificate_id:
            context['status'] = 'error'
            context['message'] = 'Please provide intern_ids or cohort_id or certificate_id'
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        try:
            certificate = Certificate.objects.get(id=certificate_id)
        except Certificate.DoesNotExist:
            context['status'] = 'error'
            context['message'] = 'Certificate does exist'
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        try:
            cohort = Cohort.objects.get(id=cohort_id)
        except Cohort.DoesNotExist:
            context['status'] = 'error'
            context['message'] = 'Cohort does exist'
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        if cohort_id:
            interns = InternProfile.objects.filter(cohort=cohort)
        else:
            interns = InternProfile.objects.filter(id__in=intern_ids)

        certificates_issued = []
        for intern in interns:
            intern.certificate_id = certificate
            intern.save()
            certificates_issued.append({
                'intern_id': intern.id,
                'certificate_id': certificate_id
            })
        
        context['status'] = 'success'
        context['certificates_issued'] = certificates_issued
        return Response(context, status=status.HTTP_200_OK)
