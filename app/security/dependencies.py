# coding: utf-8

from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import PyJWTError, ExpiredSignatureError, DecodeError
from jwt.exceptions import InvalidTokenError

from app.db import get_db
from app import models as M
from app.services.users import get_user_by_username_service
from app.utils.security import decode_jwt
from app.utils.exceptions import LoginFailedException
from app.utils.exceptions import (
    InvalidTokenException, ExpiredTokenException, TokenDecodeException
)


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl='oauth2/login',
    authorizationUrl='oauth2/authorize',
    scopes={'openid': 'OpenID Connect scope', 'profile': 'User profile'},
    auto_error=False
)


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
) -> M.User:

    try:
        payload = decode_jwt(token)
        username = payload.get('sub')

    except ExpiredSignatureError:
        raise ExpiredTokenException
    except InvalidTokenError:
        raise InvalidTokenException
    except DecodeError:
        raise TokenDecodeException

    db_user = await get_user_by_username_service(
        username=username,
        db=db
    )

    if db_user.disabled:
        raise LoginFailedException('User Disabled')

    return db_user


async def get_optional_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> M.User:

    try:
        payload = decode_jwt(token)
        username = payload['sub']

        db_user = await get_user_by_username_service(
            username=username,
            db=db
        )

        if db_user.disabled:
            raise LoginFailedException('User Disabled')
    except (PyJWTError, ExpiredSignatureError, InvalidTokenError, DecodeError):
        return None

    return db_user
