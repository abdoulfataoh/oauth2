# coding: utf-8

from fastapi import Request
from fastapi.exceptions import RequestValidationError

from app.utils.exceptions import (
    InvalidJSONFormatException, InvalidFieldsException
)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Validation errors
    """
    for error in exc.errors():
        if error['type'] == 'json_invalid':
            raise InvalidJSONFormatException
        elif error['type']:
            raise InvalidFieldsException
