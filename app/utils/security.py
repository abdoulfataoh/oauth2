# coding: utf-8

from uuid import uuid4
from passlib.context import CryptContext
import secrets
from datetime import datetime, timedelta
import pytz
import jwt

from app import settings
from app.utils.exceptions import (
    InvalidTokenException, ExpiredTokenException, TokenDecodeException
)

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


def generate_username(firstname: str, lastname: str) -> str:
    """
    Generate an username from user informations
    """
    slug = uuid4().hex[:3]
    username = f'{firstname}.{lastname}.{slug}'.lower()
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

    tz = pytz.timezone(settings.OAUTH_TIMEZONE)
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

    Raises:
        HTTPException: token exceptions.
    """
    secret_key = settings.JWT_SECRET_KEY
    jwt_algorithm = settings.JWT_ALGORITHM

    decoded_payload = jwt.decode(
            token, secret_key, algorithms=[jwt_algorithm],
            options={'verify_aud': False}
        )

    try:
        decoded_payload = jwt.decode(
            token, secret_key, algorithms=[jwt_algorithm],
            options={'verify_aud': False}
        )
        return decoded_payload

    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException
    except jwt.exceptions.InvalidTokenError:
        raise InvalidTokenException
    except jwt.DecodeError:
        raise TokenDecodeException
