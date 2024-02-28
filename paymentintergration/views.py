# import requests
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.decorators import api_view
# from django.contrib.auth import authenticate
# from django.conf import settings
# from .models import Wallet, PaymentTransaction
# from .serializers import UserSerializer, WalletSerializer, DepositSerializer


# class Login(APIView):
#     permission_classes = ()

#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         user = authenticate(username=username, password=password)
#         if user:
#             return Response({"token": user.auth_token.key, "username": username})
#         else:
#             return Response(
#                 {"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST
#             )


# class Register(APIView):
#     authentication_classes = ()
#     permission_classes = ()

#     def post(self, request):

#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data)


# class WalletInfo(APIView):
#     def get(self, request):
#         wallet = Wallet.objects.get(user=request.user)
#         data = WalletSerializer(wallet).data
#         return Response(data)


# class DepositFunds(APIView):
#     def post(self, request):
#         serializer = DepositSerializer(data=request.data, context={"request": request})
#         serializer.is_valid(raise_exception=True)

#         resp = serializer.save()
#         return Response(resp)


# class VerifyDeposit(APIView):
#     def get(self, request, reference):
#         transaction = PaymentTransaction.objects.get(
#             paystack_payment_reference=reference, wallet__user=request.user
#         )
#         reference = transaction.paystack_payment_reference
#         url = "https://api.paystack.co/transaction/verify/{}".format(reference)
#         headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        
#         r = requests.get(url, headers=headers)
#         resp = r.json()
#         if resp["data"]["status"] == "success":
#             status = resp["data"]["status"]
#             amount = resp["data"]["amount"]
#             PaymentTransaction.objects.filter(
#                 paystack_payment_reference=reference
#             ).update(status=status, amount=amount)
#             return Response(resp)
#         return Response(resp)

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests
from django.conf import settings
import json
import hmac
import hashlib
from django.http import HttpResponse
from .models import Transaction
from .serializers import TransactionSerializer

class InitiatePayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        amount = request.data.get('amount')
        email = user.email  # Assuming the user model has an email field
        callback_url = request.data.get('callback_url')

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "amount": amount,
            "email": email,
            "callback_url": callback_url,
        }
        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=data)
        return Response(response.json())

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