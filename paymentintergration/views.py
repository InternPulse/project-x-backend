# from django.shortcuts import render

# # Create your views here.

#    from rest_framework.views import APIView
#    from rest_framework.response import Response
#    from .services import PaystackService

#    class InitializeTransactionView(APIView):
#        def post(self, request):
#            amount = request.data.get('amount')
#            email = request.data.get('email')
#            callback_url = request.data.get('callback_url')
#         #    callback_url = request.build_absolute_uri(reverse('home')) 
#            paystack = PaystackService()
#            response = paystack.initialize_transaction(amount, email, callback_url)
#            return Response(response)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from django.conf import settings
from .models import Wallet , PaymentTransaction
from .serializers import WalletSerializer, DepositSerializer


class Login(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key, "username": username})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class Register(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class UserAPI(APIView):
    def get(self, request):
        user = self.request.user


        class WalletInfo(APIView):

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        data = WalletSerializer(wallet).data
        return Response(data)


class DepositFunds(APIView):

    def post(self, request):
        serializer = DepositSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        resp = serializer.save()
        return Response(resp)

class VerifyDeposit(APIView):

    def get(self, request, reference):
    transaction = PaymentTransaction.objects.get(
    paystack_payment_reference=reference, wallet__user=request.user)

    reference = transaction.paystack_payment_reference
    url = 'https://api.paystack.co/transaction/verify/{}'.format(reference)
    headers = {
        "authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }
    r = requests.get(url, headers=headers)
    resp = r.json()
    if resp['data']['status'] == 'success':

            status = resp['data']['status']
            amount = resp['data']['amount']
            PaymentTransaction.objects.filter(paystack_payment_reference=reference).update(status=status,
                                                                                        amount=amount)
            return Response(resp)
        return Response(resp)