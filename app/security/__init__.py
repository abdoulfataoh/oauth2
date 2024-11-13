# coding: utf-8

from fastapi_oauth2_service.security.encryption import Secret
from fastapi_oauth2_service.security.json_web_token import create_access_token


__all__ = [
    'secret',
    'create_access_token',
]

secret = Secret()
