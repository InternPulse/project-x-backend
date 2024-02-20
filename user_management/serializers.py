"""All serializers for the views involved in the authentication and account management process"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    EmailField,
    ImageField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    ValidationError,
)
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken

from utils import validators as v
from utils.types import AuthUser

from .models import Profile

User = get_user_model()


class CustomLoginSerializer(Serializer):
    """A custom login serializer method that uses email or username to login"""

    email = CharField(validators=[v.validate_name])
    password = CharField(validators=[v.validate_password])

    def validate(self, attrs: dict) -> dict:
        email = attrs.get("email")
        password = attrs.get("password")
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
                raise ValidationError("Invalid email/username or password")
        else:
            raise ValidationError('Must include "email" and "password".')

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        return RefreshToken.for_user(user)


class SignUpSerializer(ModelSerializer):
    """Custom signup serializer. It contains only fields that I can get from
    a google authentication and must be changed by a secure link"""

    email = EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = CharField(validators=[v.validate_name])
    last_name = CharField(validators=[v.validate_name])
    password = CharField(validators=[v.validate_password])

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict) -> AuthUser:
        """Create a new user"""
        try:
            password = validated_data.pop("password")
            validated_data["username"] = validated_data["email"]
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
        except IntegrityError as e:
            if "email" in str(e):
                raise ValidationError("User with this email already exists")
            else:
                raise ValidationError("Invalid data")
        return user


class ProfileManageSerializer(ModelSerializer):
    """Serializer for modifying your profile"""

    avatar = ImageField(required=False, validators=[v.validate_image])
    address = CharField(required=False)
    phone_number = CharField(required=False, validators=[v.validate_phone])
    country = CharField(required=False, validators=[v.validate_name])
    state = CharField(required=False, validators=[v.validate_name])
    city = CharField(required=False, validators=[v.validate_name])
    zip_code = CharField(required=False, validators=[v.validate_name])

    class Meta:
        model = Profile
        fields = [
            "avatar",
            "address",
            "phone_number",
            "country",
            "state",
            "city",
            "zip_code",
        ]


class UserManageSerializer(ModelSerializer):
    """Serializer for modifying your user information."""

    email = EmailField(
        required=False, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = CharField(required=False, validators=[v.validate_name])
    last_name = CharField(required=False, validators=[v.validate_name])
    middle_name = CharField(required=False, validators=[v.validate_name])
    role = ChoiceField(choices=User.USER_ROLES, required=False)
    id = CharField(
        read_only=True
    )  # It is an integer a big integer but it is represented as a character so that we can view it properly
    profile = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "middle_name",
            "id",
            "first_name",
            "last_name",
            "role",
            "profile",
        ]

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError as e:
            if "email" in str(e):
                raise ValidationError("A user with this email already exists")
            else:
                raise ValidationError("Invalid data")

    def get_profile(self, obj):
        if hasattr(obj, "profile"):
            return ProfileManageSerializer(obj.profile).data
        else:
            return {}


class RequestSerializer(Serializer):
    email = EmailField()


class PasswordResetSerializer(Serializer):
    password = CharField(validators=[v.validate_password])
    confirm_password = CharField(validators=[v.validate_password])


class EmptySerializer(Serializer):
    pass


class OTPSerializer(Serializer):
    otp = CharField(validators=[v.validate_otp], required=False)
    link = CharField(required=False)
    email = EmailField(required=False)

    def validate(self, data):
        token = data.get("link")
        otp = data.get("otp")
        email = data.get("email")

        if token is None and (otp is None or email is None):
            raise ValidationError("Either link or both otp and email must be provided")
        return data

class SocialLoginSerializer(ModelSerializer):
    access = CharField()
    refresh = CharField()

    class Meta:
        model = User
        fields = ["access", "refresh"]