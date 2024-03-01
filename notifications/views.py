from rest_framework import generics, status
from rest_framework.response import Response
from .models import TalentRequestTicket
from .serializers import TalentRequestTicketSerializer

# Create your views here.


class TalentRequestTicketRegistrationView(generics.CreateAPIView):
    """
    API view for talent request ticket registration.
    """

    queryset = TalentRequestTicket.objects.all()
    serializer_class = TalentRequestTicketSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = {
            "status": "success",
            "error": None,
            "message": "Talent request ticket created successfully. An acknowledgement message has been sent to your email",
            "data": serializer.data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()
