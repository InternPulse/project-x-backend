from django.contrib import admin
from .models import Notification, PaymentTicket, DefermentTicket, TalentRequestTicket

admin.site.register(Notification)
admin.site.register(PaymentTicket)
admin.site.register(DefermentTicket)
admin.site.register(TalentRequestTicket)
