from django.db import models
from utils.snowflakes import Snowflake


class BaseModel(models.Model):
    """Base model for all models in the project"""
    id = models.BigIntegerField(primary_key=True,
                                 default=Snowflake(1, 1).generate_id,
                                 editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
