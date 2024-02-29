from django.contrib.auth import get_user_model
from django.db import models
from .utils import validate_website
from utils.models import BaseModel

# Create your models here.

User = get_user_model()


class Notification(BaseModel):
    message = models.TextField(null=False)
    recipient_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class PaymentTicket(BaseModel):
    sender_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    payment_reason = models.TextField(null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        null=False,
        choices=[
            (
                "UNSUCCESSFUL",
                "Unsuccessful",
            ),
            ("PENDING", "Pending"),
            ("SUCCESSFUL", "Successful"),
        ],
        max_length=50,
        default="PENDING",
    )
    account_number = models.CharField(null=False, max_length=50)
    account_owner = models.CharField(null=False, max_length=11)
    account_bank = models.CharField(null=False, max_length=50)


class DefermentTicket(BaseModel):
    deferment_reason = models.TextField(null=True)
    sender_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.CharField(
        null=False,
        choices=[
            (
                "DECLINED",
                "Declined",
            ),
            ("PENDING", "Pending"),
            ("APPROVED", "Approved"),
        ],
        max_length=50,
        default="PENDING",
    )


class TalentRequestTicket(BaseModel):
    company_name = models.CharField(null=False, max_length=50)
    company_mail = models.EmailField(null=False, unique=False)
    company_website = models.CharField(null=False, max_length=50)
    company_requirements = models.TextField(null=False, max_length=1000)
    job_position = models.CharField(null=False, max_length=50)
    proposed_salary = models.TextField(null=False, max_length=1000)

    def __str__(self) -> str:
        return self.company_name
