"""All serializers for the views involved in the authentication and account management process"""


from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
    ValidationError,
    #  SerializerMethodField,
    Serializer,
)

from utils import validators as v
from utils.types import AuthUser
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token

User = get_user_model()

class CustomLoginSerializer(ModelSerializer):
    """A custom login serializer method that uses email or username to login"""
    email = CharField(validators=[v.validate_name])
    password = CharField(validators=[v.validate_password])

    def validate(self, attrs: dict) -> dict:
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                result = {}
                refresh = self.get_token(user)
                result["refresh"] = str(refresh)
                result["access"] = str(refresh.access_token)
                update_last_login(None, user)
                return result
            else:
                raise ValidationError('Invalid email/username or password')
        else:
            raise ValidationError('Must include "email" and "password".')

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        return RefreshToken.for_user(user)


class SignUpSerializer(ModelSerializer):
    """Custom signup serializer. It contains only fields that I can get from
    a google authentication and must be changed by a secure link"""
    email = EmailField()
    first_name = CharField(validators=[v.validate_name])
    last_name = CharField(validators=[v.validate_name])
    password = CharField(validators=[v.validate_password])

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data: dict) -> AuthUser:
        """Create a new user"""
        try:
            user = User.objects.create_user(**validated_data)
        except IntegrityError as e:
            if 'email' in str(e):
                raise ValidationError('User with this email already exists')
            else:
                raise ValidationError('Invalid data')
        return user


class UserManageSerializer(ModelSerializer):
    """Serializer for modifying your user information."""
    email = EmailField(required=False)
    first_name = CharField(required=False, validators=[v.validate_name])
    last_name = CharField(required=False, validators=[v.validate_name])
    middle_name = CharField(required=False, validators=[v.validate_name])
    class Meta:
        model = User
        fields = ['email', 'middle_name', 'id', 'first_name', 'last_name']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError as e:
            if 'email' in str(e):
                raise ValidationError('A user with this email already exists')
            else:
                raise ValidationError('Invalid data')

class RequestSerializer(Serializer):
    email = EmailField()

class PasswordResetSerializer(Serializer):
    password = CharField(validators=[v.validate_password])
    confirm_password = CharField(validators=[v.validate_password])

class EmptySerializer(Serializer):
    pass
