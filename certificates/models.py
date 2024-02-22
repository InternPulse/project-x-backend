from django.db import models
from django.utils import timezone


# Create your models here.
class Certificate(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="certificates/")
    issued_to = models.CharField(max_length=100)
    issue_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
