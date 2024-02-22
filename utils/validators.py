"""Utility validator function for """
import filetype
import re
from django.conf import settings
from rest_framework.serializers import ValidationError


def validate_name(name: str) -> bool:
    """Validates the name of a user"""
    if len(name) < 2 or len(name) > 50:
        raise ValidationError("Name should be between 2 and 50 characters")


def validate_password(password: str) -> bool:
    """Validates the password of a user"""
    if not any(x.islower() for x in password):
        raise ValidationError("Password was contain at least one lower case letter")
    if len(password) > 15 or len(password) < 6:
        raise ValidationError("Password must be between 6 and 15 characters")
    if not any(x.isdigit() for x in password):
        raise ValidationError("Password must have at least one number")
    if not any(x.isalpha() for x in password):
        raise ValidationError("Password must have at least one letter")


def validate_otp(otp: str) -> bool:
    """Validates the OTP of a user"""
    if len(otp) != settings.OTP["length"]:
        raise ValidationError(f"OTP must be {settings.OTP['length']} characters long")
    if not otp.isdigit():
        raise ValidationError("OTP must be a number")


def validate_phone(phone: str) -> bool:
    phone_regex = r"^\+\d{1,4}\s\d{1,14}$"
    if len(phone) > 20:
        raise ValidationError("Phone number must be less than 20 digits long")
    if not re.match(phone_regex, phone):
        raise ValidationError("Phone number must be in the format +234 1234567890")


def validate_image(file):
    valid_mime_types = ["image/jpeg", "image/png"]
    filesize = file.size
    valid_file_extensions = [".png", ".jpg", ".jpeg"]
    try:
        kind = filetype.guess(file)
        if filesize > 8 * 1024 * 1024:
            raise ValidationError("The maximum file size that can be uploaded is 8MB")
        if not kind:
            raise ValidationError("Unsupported file type.")
        if kind.mime not in valid_mime_types:
            raise ValidationError("Unsupported file type.")
        if kind.extension not in valid_file_extensions:
            raise ValidationError("Unacceptable file extension.")
    except TypeError as e:
        print(e)
        raise ValidationError("Unsupported file type.")
