# from django.contrib import admin
# from .models import Wallet, PaymentTransaction
# # Register your models here.

# admin.site.register(Wallet)
# admin.site.register(PaymentTransaction)

from django.contrib import admin
from .models import Transaction

# Register your models here.


admin.site.register(Transaction)
