# from django.db import models

# class Payment(models.Model):
#     amount = models.PositiveIntegerField()
#     ref = models.CharField(max_length=200)
#     email = models.EmailField()
#     verified = models.BooleanField(default=False)
#     date_created = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'deposit'),
        ('transfer', 'transfer'),
        ('withdraw', 'withdraw'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField()
    reference = models.CharField(max_length=200, unique=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.reference} by {self.email}"
        return self.user.__str__()
    

# class PaymentTransaction(BaseModel):

#     TRANSACTION_TYPES = (
#         ('deposit', 'deposit'),
#         ('transfer', 'transfer'),
#         ('withdraw', 'withdraw'),
#     )
#     wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)
#     transaction_type = models.CharField(
#         max_length=200, null=True,  choices=TRANSACTION_TYPES)
#     amount = models.DecimalField(max_digits=65, null=True, decimal_places=2)
#     timestamp = models.DateTimeField(default=timezone.now, null=True)
#     status = models.CharField(max_length=100, default="pending")
#     paystack_payment_reference = models.CharField(max_length=100, default='', blank=True)

#     def __str__(self):
#         return self.wallet.user.__str__()



# class Transaction(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     reference = models.CharField(max_length=200)
#     verified = models.BooleanField(default=False)
#     date_created = models.DateTimeField(auto_now_add=True)

#     def _str_(self):
#         return f"Payment: {self.amount}"