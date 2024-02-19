# cohort_management/models.py

from django.db import models

from user_management.models import (
    User,
)  # Import the User model from user_management app
from utils.models import BaseModel


class Cohort(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    rules = models.TextField()

    def __str__(self):
        return self.title


class InternProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)  # Choices [admin, member, ...]

    def __str__(self):
        return f"{self.user.username}'s Profile"
