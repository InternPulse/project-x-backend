# cohort_management/serializers.py

from rest_framework import serializers
from .models import Cohort, InternProfile

class InternProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the InternProfile model.

    This serializer handles the conversion of InternProfile model instances to JSON format and vice versa.
    """

    class Meta:
        model = InternProfile
        fields = '__all__'

    def validate_role(self, value):
        """
        Validate the role field.

        This method ensures that the role provided is one of the valid roles.
        """
        valid_roles = ['Product designer', 'Backend developer', 'Frontend developer', 'Product manager']
        if value not in valid_roles:
            raise serializers.ValidationError("Invalid role.")
        return value

    def validate_certificate_id(self, value):
        """
        Validate the certificate_id field.

        This method ensures that the certificate ID is a positive integer.
        """
        if value and value < 0:
            raise serializers.ValidationError("Certificate ID must be a positive integer.")
        return value

class CohortSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cohort model.

    This serializer handles the conversion of Cohort model instances to JSON format and vice versa.
    """

    class Meta:
        model = Cohort
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'created_at', 'updated_at']


    def validate_title(self, value):
        """
        Validate the title field.

        This method ensures that the title provided is at least 10 characters long.
        """
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def validate_description(self, value):
        """
        Validate the description field.

        This method ensures that the description provided is at least 10 characters long.
        """
        if len(value) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters long.")
        return value
