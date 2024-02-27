from django.db import models
from django.utils import timezone

from user_management.models import User
from cohort_management.models import Cohort

from utils.models import BaseModel


# Create your models here.
class Certificate(BaseModel):
    user = models.ForeignKey(User, 
                            related_name='user_certificate',
                            on_delete=models.DO_NOTHING,
                            blank=True, null=True)
    cohort = models.ForeignKey(Cohort, 
                                related_name='cohort_certificate',
                                on_delete=models.DO_NOTHING,
                                blank=True, null=True)
    intern_name = models.CharField(max_length=100, blank=True, null=True)
    stack = models.CharField(max_length=100, blank=True, null=True)
    is_issued = models.BooleanField(default=False)
    issue_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        if self.user:
            self.intern_name = f"{self.user.first_name} {self.user.last_name}"
            self.stack = self.user.user_profile.role
        super().save(*args, **kwargs)
