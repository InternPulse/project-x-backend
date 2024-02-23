import jwt
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
from .models import MyRefreshToken
from .pagination import CustomPagination
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)
from urllib.parse import unquote
from user_management.permissions import IsAdminPermission
from utils.otp import generate_otp_link, get_otp, verify_otp, verify_otp_link
from utils.validators import RestValidationError, get_response, ViewErrorMixin

from .backends import CustomJWTAuthentication
from .models import BLToken, Profile
from .serializers import (
    CustomLoginSerializer,
    CustomLogoutSerializer,
    EmptySerializer,
    OTPSerializer,
    PasswordResetSerializer,
    ProfileManageSerializer,
    RequestSerializer,
    SignUpSerializer,
    UserManageSerializer,
)

User = get_user_model()


def get_obj_or_rest_error(object, name, *args, **values):
    try:
        return object.objects.get(*args, **values)
    except object.DoesNotExist:
        raise RestValidationError(
            "Not found",
            {"lookup": f"The requested {name} wasn't found"},
            404,
            success=False,
        )


class LoginView(ViewErrorMixin, TokenObtainPairView):
    serializer_class = CustomLoginSerializer


class SignupView(ViewErrorMixin, CreateAPIView):
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
        refresh = MyRefreshToken.for_user(user)
        result = {}
        result["refresh"] = str(refresh)
        result["access"] = str(refresh.access_token)
        result["sub"] = str(user.id)
        decoded_token = jwt.decode(
            result["access"], options={"verify_signature": False}
        )
        result["iat"] = decoded_token.get("iat")
        result["expiry"] = decoded_token.get("exp")
        return Response(
            get_response(200, "Signup successful", result),
            status=HTTP_201_CREATED,
        )

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_create(serializer)


class LogoutView(ViewErrorMixin, TokenBlacklistView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    serializer_class = CustomLogoutSerializer

    def post(self, request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        header = request.headers.get("Authorization")
        token = header.split(" ")[1]
        BLToken.objects.create(token=token, user=request.user)
        return Response(get_response(200, "Logout successful", {}), 200)


class MyRefreshTokenView(ViewErrorMixin, TokenRefreshView):
    pass


class PasswordResetRequestView(ViewErrorMixin, GenericAPIView):
    serializer_class = RequestSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        user = get_obj_or_rest_error(User, "user", email=email)
        token = generate_otp_link(user.id, "pwd")
        link = f"{settings.FE_URL}/password-reset/{token}"
        print(link)
        sent = True  # Replace with code for emailing
        if sent:
            return Response(
                get_response(
                    200,
                    "Password reset link generated",
                    {"auth": "A reset password has been sent to your email"},
                ),
                status=HTTP_200_OK,
            )
        else:
            raise RestValidationError(
                "Email sending failed",
                {"auth": ["An error occurred. Please try again later"]},
                400,
            )


class PasswordResetConfirmView(ViewErrorMixin, GenericAPIView):
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


class RequestVerificationView(ViewErrorMixin, GenericAPIView):
    """Request for a verification link if you skipped the process during signup"""

    serializer_class = RequestSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        user = get_obj_or_rest_error(User, "user", email=email)
        token = generate_otp_link(user.id, "vyf")
        link = f"{settings.FE_URL}/activate/{token}"
        print(link)
        sent = True  # Replace with code for emailing
        if sent:
            return Response(
                get_response(
                    HTTP_200_OK,
                    "Email sent successfully",
                    {
                        "auth": "A verification mail has been successfully sent to your email"
                    },
                ),
                status=HTTP_200_OK,
            )
        else:
            raise RestValidationError(
                "Email sending failed",
                {"auth": ["An error occurred. Please try again later"]},
                400,
            )


class VerificationConfirmView(ViewErrorMixin, GenericAPIView):
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
                raise RestValidationError(
                    "Invalid token",
                    {"auth": ["Invalid or expired token"]},
                    HTTP_400_BAD_REQUEST,
                    success=False,
                )

            if not user:
                raise RestValidationError(
                    "Not found",
                    {"lookup": f"The requested user wasn't found"},
                    404,
                    success=False,
                )
        else:
            email = serializer.data.get("email")
            otp = serializer.data.get("otp")
            user = get_obj_or_rest_error(User, "user", email=email)
            if not verify_otp(user, otp):
                raise RestValidationError(
                    "Invalid otp",
                    {"auth": ["Invalid or expired otp"]},
                    HTTP_400_BAD_REQUEST,
                    success=False,
                )

        user.is_verified = True
        user.save()
        return Response(
            get_response(
                HTTP_200_OK,
                "User verified successfully",
                {"auth": "user successfully verified"},
            ),
            status=HTTP_200_OK,
        )


class UserView(ViewErrorMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserManageSerializer
    authentication_classes = [CustomJWTAuthentication]

    def get_permissions(self):
        if self.request.method in ["GET", "PATCH"]:
            return [IsAuthenticated()]
        elif self.request.method == "DELETE":
            return [IsAdminPermission()]
        return super(UserView, self).get_permissions()

    def get_object(self, pk):
        return get_obj_or_rest_error(User, "user", pk=pk)

    def get(self, request, id, *args, **kwargs):
        user = self.get_object(id)
        serializer = self.serializer_class(user)
        return Response(
            get_response(
                HTTP_200_OK,
                "User data",
                serializer.data,
            ),
            status=HTTP_200_OK,
        )

    def patch(self, request, id, *args, **kwargs) -> Response:
        current = request.user
        user = self.get_object(id)
        if "role" in request.data and current.role != "admin":
            raise RestValidationError(
                "Permission denied",
                {"permission": "You are not authorized to change user roles"},
                HTTP_403_FORBIDDEN,
                success=False,
            )
        if "role" in request.data and len(request.data) > 1 and current != user:
            raise RestValidationError(
                "Permission denied",
                {
                    "permission": "You can only change the role of another user as an admin"
                },
                HTTP_403_FORBIDDEN,
                success=False,
            )

        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
        return Response(
            get_response(
                HTTP_200_OK,
                "User modified",
                serializer.data,
            ),
            status=HTTP_200_OK,
        )

    def delete(self, request, id, *args, **kwargs) -> Response:
        user = self.get_object(id)
        deactivate = request.query_params.get("deactivate", "false").lower() == "true"
        if deactivate:
            user.is_active = False
            user.save()
        else:
            user.delete()
        return Response(
            get_response(HTTP_200_OK, "User deleted", {}),
            status=HTTP_200_OK,
        )


class UserListView(ViewErrorMixin, ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserManageSerializer
    pagination_class = CustomPagination
    queryset = User.objects.all().order_by("id")

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())

    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(
    #         get_response(
    #             HTTP_200_OK,
    #             "User list",
    #             serializer.data,
    #         ),
    #         status=HTTP_200_OK,
    #     )


class ProfileView(ViewErrorMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileManageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return get_obj_or_rest_error(Profile, "profile", user=self.request.user)

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            get_response(
                HTTP_200_OK,
                "Profile created",
                serializer.data,
            ),
            status=HTTP_200_OK,
        )

    def put(self, request, *args, **kwargs):
        raise RestValidationError(
            "Method not allowed",
            {"auth": ["You cannot perfnorm this operation"]},
            success=False,
            status=405,
        )


class GoogleLoginView(SocialLoginView):
    """This view is for logging in a user via google. It has been tweaked to also return jwt
    tokens for use in case of other clients like mobile apps, etc but it creates a session for the
    user
    It is using the defauls serializer class for the body in case we may need to deal with other
    providers in the future but this is the expected body
    ```python
    {
        "code": "4/00sdhfhdgfksnbsdfyghfgdxknkjfdhjhdjQ"
    }
    ```
    """

    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_REDIRECT_URL
    client_class = OAuth2Client

    # The next three functions are a workaround for me to return jwt tokens still even though the
    # login creates a session for the user with cookies.


class GoogleCallBackView(GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        encoded_code = request.query_params.get("code", None)
        if encoded_code:
            decoded_code = unquote(encoded_code)
            return Response({"code": decoded_code}, status=HTTP_200_OK)
        return Response(
            {"message": "No code provided or Invalid code"}, status=HTTP_400_BAD_REQUEST
        )


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """
    This view is needed by the dj-rest-auth-library in order to work the google login. It's a bug.
    """

    permanent = False

    def get_redirect_url(self):
        return "redirect-url"
