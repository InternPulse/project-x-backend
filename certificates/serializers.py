from rest_framework import serializers
from .models import Certificate


class CertificateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['user', 'cohort', 'is_issued', 'issue_date',]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if instance.user:
            instance.intern_name = f"{instance.user.first_name} {instance.user.last_name}"
            instance.stack = instance.user.user_profile.role
            instance.save()
        return instance


class CertificateIssueBatchSerializer(serializers.Serializer):
    intern_profile_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    cohort_id = serializers.IntegerField(required=False)
