from django.contrib import admin

from .models import DefermentTicket, Notification, PaymentTicket, TalentRequestTicket

admin.site.register(Notification)
admin.site.register(PaymentTicket)
admin.site.register(DefermentTicket)
admin.site.register(TalentRequestTicket)
