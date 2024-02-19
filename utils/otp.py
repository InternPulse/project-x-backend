"""This module is for generating and validating otps for
different purposes in the application. It uses the pyotp"""

from typing import Any
from django.core import signing as si
from django.conf import settings
from django.contrib.auth import get_user_model
from pyotp import TOTP
from .types import AuthUser


User = get_user_model()

def get_otp(user: AuthUser) -> str:
    """Creates a user specific otp using the user's secret key
    Args:
     user (AuthUser): The user object
    """
    otp = TOTP(user.secret, interval=settings.OTP['expiry'], digits=settings.OTP['length'])
    return otp.now()

def verify_otp(user: AuthUser, otp: str) -> bool:
    """Verifies the otp using the user's secret key. 
    Returns True if the otp is valid, False otherwise.
    Args:
     user (AuthUser): The user object
     otp (str): The otp to be verified
    Returns:
     (bool): True if the otp is valid, False otherwise
    """
    checker: TOTP = TOTP(user.secret, interval=settings.OTP['expiry'], digits=settings.OTP['length'])
    return checker.verify(otp)


def generate_otp_link(user_id: int, purpose: str):
        """Generates otp for password reset and account verification"""
        data = {
                        'user_id': user_id,
                        'for': purpose
        }
        token = si.dumps(data, compress=True)
        return token

def verify_otp_link(token: str, purpose: str):
    """Verify the generated otps for password reset and account verification"""
    try:
        data = si.loads(token, max_age=settings.TOKEN_EXPIRY)
        if purpose != data.get('for'):
            return None, 400
        user = User.objects.get(id=data.get('user_id'))
        if not user:
            return None, 404
    except (si.SignatureExpired, si.BadSignature):
        return None, 400
    return user, 200

def generate_link(data: Any) -> str:
    """Generates a safe link containing information"""
    token = si.dumps(data, compress=True)
    return token

def decrypt_link(link: str) -> Any:
    """Decrypts the link and returns the data"""
    try:
        data = si.loads(link, max_age=settings.TOKEN_EXPIRY)
    except (si.SignatureExpired, si.BadSignature):
        return None
    return data