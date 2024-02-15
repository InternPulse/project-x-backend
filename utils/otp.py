"""This module is for generating and validating otps for
different purposes in the application. It uses the pyotp"""

from django.settings import OTP
from django.contrib.auth import get_user_model
from pyotp import TOTP


User = get_user_model()




def get_otp(user: User):
    otp = TOTP(user.secret, interval=OTP['expiry'], digits=OTP['length'])
    return otp.now()

def verify_otp(user: User, otp: str):
    tp = TOTP(user.secret, interval=OTP['expiry'], digits=OTP['length'])
    return tp.verify(otp)
