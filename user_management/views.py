from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView, TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from user_management.permissions import IsAdminPermission
from .backends import CustomJWTAuthentication
from django.conf import settings
from utils.otp import generate_otp_link, verify_otp_link, verify_otp, get_otp
from django.contrib.auth import get_user_model
from .serializers import (
    CustomLoginSerializer,
    OTPSerializer,
    SignUpSerializer,
    RequestSerializer, 
    PasswordResetSerializer,
    UserManageSerializer,
)
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_204_NO_CONTENT
)
from .models import BLToken
User = get_user_model()


class LoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer


class SignupView(CreateAPIView):
    """Signs up a new user
    """
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer) -> Response:
        user = serializer.save()

        if user:
            # token = generate_otp_link(user.id, 'vyf')
            # link = f"{settings.FE_URL}/activate/{token}"
            # print(link)
            print("User created with otp", get_otp(user)) # Replace with code for emailing otp
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=HTTP_201_CREATED)

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_create(serializer)
    

class LogoutView(TokenBlacklistView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        header = request.headers.get('Authorization')
        token = header.split(' ')[1]
        BLToken.objects.create(key=token, user=request.user)
        return response


class RefreshTokenView(TokenRefreshView):
    pass


class PasswordResetRequestView(GenericAPIView):
    serializer_class = RequestSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = generate_otp_link(user.id, 'pwd')
            link = f"{settings.FE_URL}/password-reset/{token}"
            print(link)
            sent = True # Replace with code for emailing
            if sent:
                return Response({"message": "A reset password token has been sent to your email"}, status=HTTP_200_OK)
            else:
                return Response({"message": "An error occurred. Please try again later"}, status=HTTP_400_BAD_REQUEST)
        return Response({"message": "There's no user with this email"}, status=HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        token = kwargs.get('token', "")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        pwd = serializer.validated_data.get('password')
        _pwd = serializer.validated_data.get('confirm_password')

        user, status = verify_otp_link(token, 'pwd')

        if status == 400:
            return Response({'status': 'invalid or expired token'}, status=HTTP_400_BAD_REQUEST)
        if status == 400:
            return Response({'status': 'User does not exist. May have been deleted'}, status=HTTP_404_NOT_FOUND)
        if pwd != _pwd:
            return Response({'status': 'passwords do not match'}, status=HTTP_400_BAD_REQUEST)
        user.set_password(pwd)
        user.save()
        return Response({'status': 'success'}, status=HTTP_200_OK)


class RequestVerificationView(GenericAPIView):
    """Request for a verification link if you skipped the process during signup"""
    serializer_class = RequestSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = User.objects.filter(email=email).first()
        print("User found")
        if user:
            token = generate_otp_link(user.id, 'vyf')
            link = f"{settings.FE_URL}/activate/{token}"
            print(link)
            sent = True # Replace with code for emailing
            if sent:           
                return Response({"message": "A verification token has been sent to your email"}, status=HTTP_200_OK)
            else:
                return Response({"message": "An error occurred. Please try again later"}, status=HTTP_400_BAD_REQUEST)
        return Response({"message": "There's no user with this email"}, status=HTTP_400_BAD_REQUEST)


class VerificationConfirmView(GenericAPIView):
    """Verify your account via a link sent to your email"""
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = OTPSerializer
    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if "token" in serializer.data:
            user, status = verify_otp_link(serializer.data["token"], 'vyf')
            if status == 400:
                return Response({'status': 'invalid or expired token'}, status=HTTP_400_BAD_REQUEST)
            if not user:
                return Response({'status': 'User does not exist. May have been deleted'}, status=HTTP_404_NOT_FOUND)
        else:
            email = serializer.data.get('email')
            otp = serializer.data.get('otp')
            user = get_object_or_404(User, email=email)
            if not verify_otp(user, otp):
                return Response({'status': 'invalid otp'}, status=HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.save()
        return Response({'status': 'success'}, status=HTTP_200_OK)


class UserView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserManageSerializer


    def get_permissions(self):
        if self.request.method in ['GET', 'PATCH']:
            return [IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [IsAdminPermission()]
        return super(UserView, self).get_permissions()

    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, id, *args, **kwargs):
        user = self.get_object(id)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def patch(self, request, id, *args, **kwargs) -> Response:
        current = request.user
        user = self.get_object(id)
        if "role" in request.data and current.role != "admin":
            return Response({"message": "You are not authorized to change user roles"}, status=HTTP_403_FORBIDDEN)
        if "role" in request.data and len(request.data) > 1 and current != user:
            return Response({"message": "You can only change the role of another user as an admin"}, status=HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)

    def delete(self, request, id, *args, **kwargs) -> Response:
        user = self.get_object(id)
        deactivate = request.query_params.get('deactivate', 'false').lower() == 'true'
        if deactivate:
            user.is_active = False
            user.save()
        else:
            user.delete()
        return Response({}, status=HTTP_204_NO_CONTENT)


class UserListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserManageSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            pass
        return get_user_model().objects.all()
        # return get_user_model().objects.filter(id=user.id)

