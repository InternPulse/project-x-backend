from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.models import BaseModel

class User(AbstractUser, BaseModel):
    """Custom user model"""
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True, default="")
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=50, default='user')

    def __str__(self):
        return f'User - {self.email} {self.id}'

    @property
    def full_name(self):
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}"

    class Meta:
        abstract = False




