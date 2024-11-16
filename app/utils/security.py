# coding: utf-8

from passlib.hash import bcrypt
from hashlib import sha256
import secrets
from datetime import datetime, timedelta
import pytz
import jwt

from app import settings


__all__ = [
    'hash', 'verify_hash', 'generate_secret',
    'generate_username', 'generate_username',
    'create_jwt',
]


def hash(secret: str) -> str:
    """
    Hash a given secret
    """
    hash = bcrypt.hash(secret)
    return hash


def verify_hash(secret: str, hash: str) -> bool:
    """
    Check is secret and hashed secret match
    """
    status = bcrypt.verify(secret, hash)
    return status


def generate_secret(length: int = 32) -> str:
    """
    Generate a random secret size = length
    """
    secret = secrets.token_urlsafe(length)
    return secret


def generate_username(firstname: str, lastname: str, phone_number) -> str:
    """
    Generate an username from user informations
    """
    combo = f'{firstname}_{lastname}_{phone_number}'.lower().encode()
    combo_hash = sha256(combo).hexdigest()
    username = f'{firstname}.{lastname}.{combo_hash[:8]}'.lower()
    return username


def create_jwt(user_id: str, expires_in: int = 3600) -> str:
    """
    Create signed JSON Web Token (JWT).

    Args:
        user_id (str): user (or entity) id
        expires_in (int): token expire date

    Returns:
        str: signed JWT.
    """

    tz = pytz.timezone(settings.TIMEZONE)
    secret_key = settings.SECRET_KEY
    jwt_algorithm = settings.JWT_ALGORITHM

    payload = {
        'sub': user_id,
        'iat': datetime.now(tz=tz),
        'exp': datetime.now(tz=tz) + timedelta(seconds=expires_in),
    }

    token = jwt.encode(payload, secret_key, algorithm=jwt_algorithm)

    return token
