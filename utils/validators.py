"""Utility validator function for """
from typing import Dict, Optional
from collections.abc import Mapping
# import filetype
import re
from django.conf import settings
from rest_framework.serializers import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.fields import (empty, get_error_detail)
from rest_framework.settings import api_settings

class RestValidationError(ValidationError):
    """A custom validation error to follow our rest convention"""
    def __init__(self, message: str, errors: Dict[str, list], status: int = 400, data: Dict[str, any] = {}, success: Optional[bool] = True):
        super().__init__(message)
        self.status = status
        self.status_code = status
        self.success = success
        self.errors = errors
        self.message = message
        self.data = data
        self.detail = self.as_dict()
    def as_dict(self):
        error_dict = {
            "status": self.status,
            "success": self.success,
            "errors": self.errors,
            "message": self.message,
            "data": self.data
        }
        return error_dict

class SerializerErrorMixin():
    err_message = "Validation failed"
    def run_validation(self, data=empty):
        """
        We override the default `run_validation`, because the validation
        performed by validators and the `.validate()` method should
        be coerced into an error dictionary with a 'non_fields_error' key.
        """
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data

        value = self.to_internal_value(data)
        try:
            self.run_validators(value)
            value = self.validate(value)
            assert value is not None, '.validate() should return the validated data'
        except (ValidationError, DjangoValidationError) as exc:
            raise RestValidationError(self.err_message, self.get_error_detail(exc), success=False)


        return value
    def is_valid(self, *, raise_exception=False):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except (RestValidationError, ValidationError) as exc:
                if isinstance(exc, RestValidationError):
                    raise exc
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise RestValidationError(self.err_message, self.errors, success=False)

        return not bool(self._errors)
    def get_error_detail(self, exc):
        print("Exc", type(exc))
        assert isinstance(exc, (ValidationError, DjangoValidationError))

        if isinstance(exc, DjangoValidationError):
            detail = get_error_detail(exc)
        else:
            detail = exc.detail

        if isinstance(detail, Mapping):
            return {
                key: value if isinstance(value, (list, Mapping)) else [value]
                for key, value in detail.items()
            }
        elif isinstance(detail, list):
            return {
                api_settings.NON_FIELD_ERRORS_KEY: detail
        }
        return {
            api_settings.NON_FIELD_ERRORS_KEY: [detail]
        }
class ViewErrorMixin():
    def permission_denied(self, request, message=None, code=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        """
        if request.authenticators and not request.successful_authenticator:
            raise RestValidationError(
                "Not authorized",
                {"auth": "Authentication credentials were not provided"},
                401,
                success=False
            )
        raise RestValidationError(
            "Not permitted",
            {"permission": "You do not have sufficient authorization for this action"},
            403,
            success=False
        )
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
    pass
    # valid_mime_types = ["image/jpeg", "image/png"]
    # filesize = file.size
    # valid_file_extensions = [".png", ".jpg", ".jpeg"]
    # try:
    #     kind = filetype.guess(file)
    #     if filesize > 8 * 1024 * 1024:
    #         raise ValidationError("The maximum file size that can be uploaded is 8MB")
    #     if not kind:
    #         raise ValidationError("Unsupported file type.")
    #     if kind.mime not in valid_mime_types:
    #         raise ValidationError("Unsupported file type.")
    #     if kind.extension not in valid_file_extensions:
    #         raise ValidationError("Unacceptable file extension.")
    # except TypeError as e:
    #     print(e)
    #     raise ValidationError("Unsupported file type.")
    

def get_response(status: int, message: str, data: Optional[Dict[str, any]] = {}, errors: Optional[Dict[str, any]] = {}, success: Optional[bool] = True):
    """Generate a default response for each user"""
    response = {
        "status": status,
        "success": success,
        "errors": errors,
        "message": message,
        "data": data
    }
    return response

