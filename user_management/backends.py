"""A wrapper class around the default JWTAuthentication class to check 
if the token is blacklisted before authenticating the user"""

from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.validators import RestValidationError
from .models import BLToken

User = get_user_model()


class CustomJWTAuthentication(JWTAuthentication):
    """Custom JWT authentication, same as the one provided by rest_framework simplejwt except
    that it checks for any blacklisted access token first"""

    def authenticate(self, request):
        """Checks if the token was recently blacklisted"""
        result = None
        try:
            result = super().authenticate(request)
        except Exception as e:
            print(e)
            raise RestValidationError(
                "Token Error",
                {
                    "auth": ["Invalid or expired token"]
                },
                401,
                success = False
            )
        header = self.get_header(request)
        if result:
            token = self.get_raw_token(header).decode("utf-8")
            if BLToken.objects.filter(token=token).exists():
                raise RestValidationError(
                    "Token Errors",
                    {
                        "auth": ["Token is blacklisted"]
                    },
                    401,
                    success = False
                )
        return result
