from rest_framework import serializers
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'


class CertificateIssueBatchSerializer(serializers.Serializer):
    intern_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    cohort_id = serializers.IntegerField(required=False)
    certificate_id = serializers.IntegerField(required=False)
