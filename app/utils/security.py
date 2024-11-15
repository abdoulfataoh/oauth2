# coding: utf-8

from passlib.hash import bcrypt
from hashlib import sha256
import secrets
from typing import Any, Optional
from datetime import datetime, timedelta
import pytz
import jwt

from app import settings


__all__ = [
    'Secret',
]


class Secret:
    """
    Collection of tools to manage secrets
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def hash(secret: str) -> str:
        hash = bcrypt.hash(secret)
        return hash

    @staticmethod
    def verify_hash(secret: str, hash: str) -> bool:
        status = bcrypt.verify(secret, hash)
        return status

    @staticmethod
    def generate_secret(length: int = 32) -> str:
        secret = secrets.token_urlsafe(length)
        return secret

    @staticmethod
    def create_access_token(
        data: dict[Any, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        tz = pytz.timezone(settings.TIMEZONE)
        secret_key = settings.OAUTH2_SECRET_KEY
        algorithm = settings.OAUTH2_ALGORITHM
        now = datetime.now(tz)

        if expires_delta:
            expire = now + expires_delta
        else:
            expire = now + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt


def generate_username(firstname: str, lastname: str, phone_number) -> str:
    """
    Generate an username from user informations
    """
    combo = f'{firstname}_{lastname}_{phone_number}'.lower()
    combo_hash = sha256(combo).hexdigest()
    username = f'{firstname}.{lastname}.{combo_hash[:8]}'
    return username
