from django.urls import path

from .views import (
    GoogleLoginView,
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    ProfileView,
    RefreshTokenView,
    RequestVerificationView,
    SignupView,
    UserListView,
    UserView,
    VerificationConfirmView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("google/login/", GoogleLoginView.as_view(), name="google-login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:id>/", UserView.as_view(), name="user-detail"),
    path("verify/", VerificationConfirmView.as_view(), name="verify-confirm"),
    path(
        "request-verification/",
        RequestVerificationView.as_view(),
        name="request-verification",
    ),
    path(
        "reset-password/",
        PasswordResetConfirmView.as_view(),
        name="reset-password-confirm",
    ),
    path(
        "request-reset-password/",
        PasswordResetRequestView.as_view(),
        name="request-reset-password",
    ),
    path("refresh-token/", RefreshTokenView.as_view(), name="refresh-token"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
