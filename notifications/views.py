from rest_framework import generics
from .models import TalentRequestTicket
from .serializers import TalentRequestTicketSerializer

# Create your views here.


class TalentRequestTicketRegistrationView(generics.CreateAPIView):
    """
    API view for talent request ticket registration.
    """

    queryset = TalentRequestTicket.objects.all()
    serializer_class = TalentRequestTicketSerializer
