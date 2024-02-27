from django.urls import path
from .views import InitiatePayment, PaystackWebhook

urlpatterns = [
    path('initiate-payment/', InitiatePayment.as_view(), name='initiate-payment'),
    path('webhook/', PaystackWebhook.as_view(), name='paystack-webhook'),
]