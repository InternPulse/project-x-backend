# cohort_management/serializers.py

from rest_framework import serializers
from .models import Cohort, InternProfile

class CohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = '__all__'

class InternProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternProfile
        fields = '__all__'
