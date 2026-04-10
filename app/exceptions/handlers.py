# flake8: noqa: F403,F405
# coding: utf-8

from typing import cast
import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.exceptions.domain import DomainException

logger = logging.getLogger(__name__)



# VALIDATION HANDLER
async def validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
):
    """
    Handle Pydantic validation errors and return only the first error.
    """

    error = exception.errors()[0]

    field = '.'.join(str(x) for x in error['loc'][1:])
    message = error['msg']

    logger.warning(f'Validation error on {request.url}: {field} -> {message}')

    return JSONResponse(
        status_code=422,
        content={
            'error': 'VALIDATION_ERROR',
            'message': f'{field}: {message}',
        },
    )


# DOMAIN HANDLER
async def domain_exception_handler(request: Request, exception: Exception):
    """
    Handle domain exceptions (clean, no mapper).
    """

    domain_exception = cast(DomainException, exception)

    logger.warning(
        f'Domain error: {domain_exception.error_code} - '
        f'{domain_exception.message} - path={request.url}'
    )

    return JSONResponse(
        status_code=domain_exception.get_status_code(),
        content={
            'error': domain_exception.error_code,
            'message': domain_exception.message,
        },
    )


# INTERNAL ERROR HANDLER
async def internal_exception_handler(request: Request, exception: Exception):
    """
    Handle unexpected errors (500).
    """

    logger.exception(f'Unhandled error on {request.url}: {exception}')

    return JSONResponse(
        status_code=500,
        content={
            'error': 'INTERNAL_SERVER_ERROR',
            'message': 'Something went wrong',
        },
    )


# REGISTER HANDLERS
def register_exception_handlers(app):
    """
    Register all exception handlers.
    """

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(DomainException, domain_exception_handler)
    app.add_exception_handler(Exception, internal_exception_handler)
