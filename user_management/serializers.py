
"""All serializers for the views involved in the authentication and account management process"""

from typing import Any, Dict
import jwt
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
    BooleanField
)
from rest_framework.validators import UniqueValidator
from .models import MyRefreshToken
from utils import validators as v
from utils.types import AuthUser

from .models import Profile, Questionnaire

User = get_user_model()


class CustomLoginSerializer(v.SerializerErrorMixin, Serializer):
    """A custom login serializer method that uses email or username to login"""

    email = EmailField(required=True)
    password = CharField(validators=[v.validate_password], required=True)

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
                result["sub"] = str(user.id)

                decoded_token = jwt.decode(
                    result["access"], options={"verify_signature": False}
                )
                result["iat"] = decoded_token.get("iat")
                result["expiry"] = decoded_token.get("exp")
                update_last_login(None, user)
                return v.get_response(200, "Login successful", result)
            else:
                raise ValidationError(
                    {"auth":"Invalid email or password"},
                )

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        return MyRefreshToken.for_user(user)


class CustomLogoutSerializer(v.SerializerErrorMixin, Serializer):
    refresh = CharField(write_only=True)
    token_class = MyRefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        try:
            refresh = self.token_class(attrs["refresh"])
            refresh.check_blacklist()
        except Exception as e:
            raise ValidationError({"refresh": [e]})
        try:
            refresh.blacklist()
        except AttributeError:
            pass
        return {}

class SignUpSerializer(v.SerializerErrorMixin, ModelSerializer):
    """Custom signup serializer. It contains only fields that I can get from
    a google authentication and must be changed by a secure link"""

    email = EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())], required=True
    )
    first_name = CharField(validators=[v.validate_name], required=True)
    last_name = CharField(validators=[v.validate_name], required=True)
    password = CharField(validators=[v.validate_password], required=True)
    questionnaire_id = CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password", "questionnaire_id")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict) -> AuthUser:
        """Create a new user"""
        try:
            password = validated_data.pop("password")
            validated_data["username"] = validated_data["email"]
            questionnaire_id = validated_data.pop("questionnaire_id", None)
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            if questionnaire_id:
                try:
                    questionnaire = Questionnaire.objects.get(id=int(questionnaire_id))
                    questionnaire.user = user
                    questionnaire.save()
                except Questionnaire.ObjectDoesNotExist:
                    pass
        except IntegrityError as e:
            if "email" in str(e):
                raise v.RestValidationError(
                    "Duplicate user entry",
                    {"email": ["A user with this email already exists"]},
                    success=False,
                    status=409,
                )
            else:
                raise v.RestValidationError(
                    "Signing up failed",
                    {"user": ["Something went wrong please try again later"]},
                    success=False,
                    status=500,
                )
        return user


class ProfileManageSerializer(v.SerializerErrorMixin, ModelSerializer):
    """Serializer for modifying your profile"""

    address = CharField(required=False)
    phone_number = CharField(required=False, validators=[v.validate_phone])
    country = CharField(required=False, validators=[v.validate_name])
    state = CharField(required=False, validators=[v.validate_name])
    city = CharField(required=False, validators=[v.validate_name])
    zip_code = CharField(required=False, validators=[v.validate_name])

    career_path = CharField(max_length=150, required=False)
    linkedin_url = CharField(validators=[v.validate_url], required=False)
    github_url = CharField(validators=[v.validate_url], required=False)
    x_url = CharField(validators=[v.validate_url], required=False)
    occupation = CharField(max_length=100, required=False)
    can_share_PI = BooleanField(default=False, required=False)

    class Meta:
        model = Profile
        fields = [
            "address",
            "phone_number",
            "country",
            "state",
            "city",
            "zip_code",

            "career_path",
            "linkedin_url",
            "github_url",
            "x_url",
            "occupation",
            "can_share_PI"
        ]


class UserManageSerializer(v.SerializerErrorMixin, ModelSerializer):
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
                raise v.RestValidationError(
                    "Duplicate user entry",
                    {"email": ["A user with this email already exists"]},
                    success=False,
                    status=409,
                )
            else:
                raise v.RestValidationError(
                    "User update failed",
                    {"user": ["Something went wrong please try again later"]},
                    success=False,
                    status=500,
                )

    def get_profile(self, obj):
        if hasattr(obj, "profile"):
            return ProfileManageSerializer(obj.profile).data
        else:
            return {}

class RequestSerializer(v.SerializerErrorMixin, Serializer):
    email = EmailField()


class PasswordResetSerializer(v.SerializerErrorMixin, Serializer):
    password = CharField(validators=[v.validate_password])
    confirm_password = CharField(validators=[v.validate_password])


class EmptySerializer(Serializer):
    pass


class OTPSerializer(v.SerializerErrorMixin, Serializer):
    otp = CharField(validators=[v.validate_otp])
    # link = CharField(required=False)
    email = EmailField()


class SocialLoginSerializer(v.SerializerErrorMixin, ModelSerializer):
    access = CharField()
    refresh = CharField()

    class Meta:
        model = User
        fields = ["access", "refresh"]


class QuestionnaireSerializer(v.SerializerErrorMixin, ModelSerializer):
    has_experience_programming = BooleanField(default=False)
    worked_on_real_life_problems = BooleanField(default=False)
    reason_for_joining_Internpulse = CharField(required=True)
    importance_of_work_exp = CharField(required=True)
    user = SerializerMethodField()
    id = CharField(read_only=True)

    class Meta:
        model = Questionnaire
        fields = [
            "id",
            "created_at",
            "user",
            "has_experience_programming",
            "worked_on_real_life_problems",
            "reason_for_joining_Internpulse",
            "importance_of_work_exp",
        ]

    def get_user(self, obj):
        if hasattr(obj, "user"):
            user_data = UserManageSerializer(obj.user).data
            user_data.pop("profile", {})
            return user_data
        else:
            return {}
