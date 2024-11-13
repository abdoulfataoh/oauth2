# coding: utf-8

from passlib.hash import bcrypt
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

    def hash(self, secret: str) -> str:
        hash = bcrypt.hash(secret)
        return hash

    def verify_hash(self, secret: str, hash: str) -> bool:
        status = bcrypt.verify(secret, hash)
        return status

    def generate_secret(self, length: int = 32) -> str:
        secret = secrets.token_urlsafe(length)
        return secret

    def create_access_token(
            self, data: dict[Any, Any], 
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
