# cohort_management/models.py

from django.db import models
from user_management.models import User
from utils.models import BaseModel


class Cohort(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    rules = models.TextField()

    def __str__(self):
        return self.title

class InternProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='interns')
    role_choices = [
        ('Product designer', 'Product designer'),
        ('Backend developer', 'Backend developer'),
        ('Frontend developer', 'Frontend developer'),
        ('Product manager', 'Product manager'),
    ]
    role = models.CharField(max_length=50, choices=role_choices)
    certificate_id = models.BigIntegerField(null=True)  # Reference to Certificate model

    def __str__(self):
        return f"{self.user.username}'s Profile"
