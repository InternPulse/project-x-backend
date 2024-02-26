"""Models relating to user management"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from pyotp import random_base32

from utils.models import BaseModel
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework.serializers import ValidationError
class User(AbstractUser, BaseModel):
    """Custom user model"""

    USER_ROLES = (("admin", "Admin"), ("intern", "intern"))

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, default="")
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=50, default="intern", choices=USER_ROLES)
    secret = models.CharField(max_length=100, default=random_base32)

    def __str__(self):
        return f"User - {self.email} {self.id}"

    @property
    def full_name(self):
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}"

    class Meta:
        abstract = False


class BLToken(BaseModel):
    """Blacklisted token model"""

    token = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Blacklisted token - {self.token}"

    class Meta:
        abstract = False


class Profile(BaseModel):
    """Profile model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, default="")
    phone_number = models.CharField(max_length=15, blank=True, default="")
    country = models.CharField(max_length=150, blank=True, default="")
    state = models.CharField(max_length=150, blank=True, default="")
    city = models.CharField(max_length=150, blank=True, default="")
    zip_code = models.CharField(max_length=10, blank=True, default="")
    tech_stack = models.JSONField(blank=True, default=dict)
    career_path = models.CharField(max_length=150, blank=True, default="")
    linkedin_url = models.CharField(max_length=150, blank=True, default="")
    github_url = models.CharField(max_length=150, blank=True, default="")
    x_url = models.CharField(max_length=150, blank=True, default="")
    occupation = models.CharField(max_length=150, blank=True, default="")
    can_share_PI = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile - {self.user.full_name}"

    class Meta:
        abstract = False

class Questionnaire(BaseModel):
    """Questionnaire model"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="questionnaire_reply", null=True)
    has_experience_programming = models.BooleanField(default=False)
    worked_on_real_life_problems = models.BooleanField(default=False)
    reason_for_joining_Internpulse = models.TextField(default="", blank=True)
    importance_of_work_exp = models.TextField()

    def __str__(self):
        return f"Survey filled by {self.user.full_name or 'anonymous'}"
    
    class Meta:
        abstract = False


class MyRefreshToken(RefreshToken):
    def check_blacklist(self) -> None:
        """
        Checks if this token is present in the token blacklist.  Raises
        `TokenError` if so.
        """
        jti = self.payload[api_settings.JTI_CLAIM]

        if BlacklistedToken.objects.filter(token__jti=jti).exists():
            raise Exception("Token is blacklisted")
