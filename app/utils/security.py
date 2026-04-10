# coding: utf-8

from uuid import uuid4
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from app import settings

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def generate_secret(length: int = 16) -> str:
    """
    Generate a random secret size = length
    """
    secret = secrets.token_urlsafe(length)
    return secret


def generate_otp() -> str:
    return str(secrets.randbelow(900000) + 100000)


def generate_username(firstname: str, lastname: str) -> str:
    """
    Generate an username from user informations
    """
    slug = uuid4().hex[:3]
    username = f'{firstname}.{lastname}.{slug}'.lower()
    username = username.replace(' ', '')
    return username


def create_jwt(expires_in: int = 3600, **kwargs):
    """
    Create signed JSON Web Token (JWT).

    Args:
        expires_in (int): token expire date
        kwargs: eg client_id, aud, scope, ...

    Returns:
        str: signed JWT.
    """

    tz = timezone.utc
    secret_key = settings.JWT_SECRET_KEY
    jwt_algorithm = settings.JWT_ALGORITHM

    payload = {
        'iat': datetime.now(tz=tz),
        'exp': datetime.now(tz=tz) + timedelta(seconds=expires_in),
    }

    payload.update(kwargs)

    token = jwt.encode(payload, secret_key, algorithm=jwt_algorithm)
    return token


def decode_jwt(token: str) -> dict:
    """
    Decode signed JSON Web Token (JWT).

    Args:
        token (str): JWT to decode.

    Returns:
        dict: jwt paylod.
    """
    secret_key = settings.JWT_SECRET_KEY
    jwt_algorithm = settings.JWT_ALGORITHM

    decoded_payload = jwt.decode(
            token, secret_key, algorithms=[jwt_algorithm],
            options={'verify_aud': False}
        )

    decoded_payload = jwt.decode(
        token, secret_key, algorithms=[jwt_algorithm],
        options={'verify_aud': False}
    )
    return decoded_payload
