from django.db import models
from django.utils import timezone

from utils.snowflakes import Snowflake


class BaseModel(models.Model):
    """Base model for all models in the project"""

    id = models.BigIntegerField(
        primary_key=True, default=Snowflake(1, 1).generate_id, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Override the save method to update the updated_at field"""
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    @classmethod
    def new(cls, *args, **kwargs):
        """Override the new method to update the created_at field"""
        instance = cls.objects.create(*args, **kwargs)
        return instance
