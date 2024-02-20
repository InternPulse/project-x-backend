from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from user_management.permissions import IsAdminPermission
from utils.otp import generate_otp_link, get_otp, verify_otp, verify_otp_link

from .backends import CustomJWTAuthentication
from .models import BLToken, Profile
from .serializers import (
    CustomLoginSerializer,
    OTPSerializer,
    PasswordResetSerializer,
    ProfileManageSerializer,
    RequestSerializer,
    SignUpSerializer,
    UserManageSerializer,
)

User = get_user_model()


class LoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer


class SignupView(CreateAPIView):
    """Signs up a new user"""

    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer) -> Response:
        user = serializer.save()

        if user:
            # token = generate_otp_link(user.id, 'vyf')
            # link = f"{settings.FE_URL}/activate/{token}"
            # print(link)
            print(
                "User created with otp", get_otp(user)
            )  # Replace with code for emailing otp
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=HTTP_201_CREATED,
        )

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_create(serializer)


class LogoutView(TokenBlacklistView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        header = request.headers.get("Authorization")
        token = header.split(" ")[1]
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
        email = serializer.validated_data.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            token = generate_otp_link(user.id, "pwd")
            link = f"{settings.FE_URL}/password-reset/{token}"
            print(link)
            sent = True  # Replace with code for emailing
            if sent:
                return Response(
                    {"message": "A reset password token has been sent to your email"},
                    status=HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "An error occurred. Please try again later"},
                    status=HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"message": "There's no user with this email"}, status=HTTP_400_BAD_REQUEST
        )


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        token = kwargs.get("token", "")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        pwd = serializer.validated_data.get("password")
        _pwd = serializer.validated_data.get("confirm_password")

        user, status = verify_otp_link(token, "pwd")

        if status == 400:
            return Response(
                {"status": "invalid or expired token"}, status=HTTP_400_BAD_REQUEST
            )
        if status == 400:
            return Response(
                {"status": "User does not exist. May have been deleted"},
                status=HTTP_404_NOT_FOUND,
            )
        if pwd != _pwd:
            return Response(
                {"status": "passwords do not match"}, status=HTTP_400_BAD_REQUEST
            )
        user.set_password(pwd)
        user.save()
        return Response({"status": "success"}, status=HTTP_200_OK)


class RequestVerificationView(GenericAPIView):
    """Request for a verification link if you skipped the process during signup"""

    serializer_class = RequestSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        user = User.objects.filter(email=email).first()
        print("User found")
        if user:
            token = generate_otp_link(user.id, "vyf")
            link = f"{settings.FE_URL}/activate/{token}"
            print(link)
            sent = True  # Replace with code for emailing
            if sent:
                return Response(
                    {"message": "A verification token has been sent to your email"},
                    status=HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "An error occurred. Please try again later"},
                    status=HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"message": "There's no user with this email"}, status=HTTP_400_BAD_REQUEST
        )


class VerificationConfirmView(GenericAPIView):
    """Verify your account via a link sent to your email"""

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if "token" in serializer.data:
            user, status = verify_otp_link(serializer.data["token"], "vyf")
            if status == 400:
                return Response(
                    {"status": "invalid or expired token"}, status=HTTP_400_BAD_REQUEST
                )
            if not user:
                return Response(
                    {"status": "User does not exist. May have been deleted"},
                    status=HTTP_404_NOT_FOUND,
                )
        else:
            email = serializer.data.get("email")
            otp = serializer.data.get("otp")
            user = get_object_or_404(User, email=email)
            if not verify_otp(user, otp):
                return Response({"status": "invalid otp"}, status=HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.save()
        return Response({"status": "success"}, status=HTTP_200_OK)


class UserView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserManageSerializer

    def get_permissions(self):
        if self.request.method in ["GET", "PATCH"]:
            return [IsAuthenticated()]
        elif self.request.method == "DELETE":
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
            return Response(
                {"message": "You are not authorized to change user roles"},
                status=HTTP_403_FORBIDDEN,
            )
        if "role" in request.data and len(request.data) > 1 and current != user:
            return Response(
                {"message": "You can only change the role of another user as an admin"},
                status=HTTP_403_FORBIDDEN,
            )
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)

    def delete(self, request, id, *args, **kwargs) -> Response:
        user = self.get_object(id)
        deactivate = request.query_params.get("deactivate", "false").lower() == "true"
        if deactivate:
            user.is_active = False
            user.save()
        else:
            user.delete()
        return Response({}, status=HTTP_204_NO_CONTENT)


class UserListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserManageSerializer
    queryset = User.objects.all().order_by("id")

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            pass
        return get_user_model().objects.all()
        # return get_user_model().objects.filter(id=user.id)


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileManageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT", detail="PUT method is not allowed on this route")


class GoogleLoginView(SocialLoginView):
    """This view is for logging in a user via google. It has been tweaked to also return jwt
    tokens for use in case of other clients like mobile apps, etc but it creates a session for the
    user"""
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_REDIRECT_URL
    client_class = OAuth2Client

    # The next three functions are a workaround for me to return jwt tokens still even though the
    # login creates a session for the user with cookies.
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.user
        token = self.get_token(user)
        data = token

        # Check if the user was just created
        if self.token.login.is_new:
            data['message'] = 'Welcome! Thanks for creating an account.'

        return Response(data)

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class UserRedirectView(LoginRequiredMixin, RedirectView):
    """
    This view is needed by the dj-rest-auth-library in order to work the google login. It's a bug.
    """

    permanent = False

    def get_redirect_url(self):
        return "redirect-url"