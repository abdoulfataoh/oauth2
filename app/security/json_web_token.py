# coding: utf-8

from typing import Any

from datetime import datetime, timedelta
from typing import Optional
import pytz
import jwt

from fastapi_oauth2_service import settings


__all__ = [
    'create_access_token',
]


def create_access_token(data: dict[Any, Any], expires_delta: Optional[timedelta] = None) -> str:
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
