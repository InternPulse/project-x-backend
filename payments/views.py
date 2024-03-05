from django.shortcuts import render

# Create your views here.
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import requests
from django.conf import settings
import json
import hmac
import hashlib
from django.http import HttpResponse
from .models import Transaction
from .serializers import TransactionSerializer

class InitiatePayment(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def generate_unique_reference():
        # Generates a unique reference using UUID
        return str(uuid.uuid4())

    def post(self, request):
        email = request.data.get('email')  # Get email from request data
        if not email:
            return Response({"error": "Email is required"}, status=400)
        amount = request.data.get('amount')
        callback_url = request.data.get('callback_url')
        reference = self.generate_unique_reference()  # Ensure this method exists

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email": email,
            "amount": amount,
            "callback_url": callback_url,
            "reference": reference,
        }
        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=data)
        # Check the response from Paystack
        if response.status_code == 200:
            # Payment initialized successfully
            return Response(response.json(), status=response.status_code)
        else:
            # Paystack returned an error
            return Response(response.json(), status=response.status_code)

# class PaystackWebhook(APIView):
#     permission_classes = []  # No authentication required

#     def post(self, request):
#         # Verify event with Paystack
#         # Update your transaction model based on the webhook data
#         return Response({"message": "Webhook received"})


class PaystackWebhook(APIView):
    permission_classes = []  # No authentication required

    def post(self, request):
        # Verify Paystack signature
        paystack_signature = request.headers.get('x-paystack-signature')
        if not paystack_signature:
            return HttpResponse(status=400)

        # Compute hash and verify signature
        computed_hash = hmac.new(
            settings.PAYSTACK_SECRET_KEY.encode('utf-8'),
            request.body,
            hashlib.sha512
        ).hexdigest()

        if paystack_signature != computed_hash:
            return HttpResponse(status=400)

        # Process webhook data
        data = json.loads(request.body)
        if data['event'] == 'charge.success':
            reference = data['data']['reference']
            try:
                transaction = Transaction.objects.get(reference=reference)
                transaction.verified = True
                transaction.save()
                # Additional logic for successful verification
            except Transaction.DoesNotExist:
                pass  # Handle error or log

        return Response({"message": "Webhook received"})