from dataclasses import dataclass, field
from typing import Type

from django.contrib.auth.models import AbstractBaseUser

AuthUser = Type[AbstractBaseUser]


from jsonschema import validate, ValidationError
response_schema = {
    "type": "object",
    "properties": {
        "status": {"type": "integer"},
        "success": {"type": "boolean"},
        "errors": {"type": "object"},
        "message": {"type": "string"},
        "data": {"type": "object"},
    },
    "required": ["status", "success", "errors", "message", "data"],
}
list_schema = {
    "type": "object",
    "properties": {
        "status": {"type": "integer"},
        "success": {"type": "boolean"},
        "errors": {"type": "object"},
        "message": {"type": "string"},
        "data": {"type": "array"},
        "page_info": {"type":"object"},
    },
    "required": ["status", "success", "errors", "message", "data", "page_info"],
}
def test_response_schema(response, is_list:bool =False):
    try:
        schema = list_schema if is_list else response_schema
        validate(instance=response, schema=schema)
    except ValidationError as e:
        return False
    return True

