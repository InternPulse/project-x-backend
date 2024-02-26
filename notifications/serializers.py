from rest_framework import serializers
from .models import TalentRequestTicket


class TalentRequestTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentRequestTicket
        fields = "__all__"

    def create(self, validated_data):
        """
        Create and return a new TalentRequestTicket instance.
        """
        return TalentRequestTicket.objects.create(**validated_data)
