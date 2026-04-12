# coding: utf-8

from typing import Annotated

from fastapi import Request, Depends, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.ext.asyncio import AsyncSession

from jwt import ExpiredSignatureError, DecodeError
from jwt.exceptions import InvalidTokenError as JWTInvalidTokenError

from app.db import get_db
from app import crud, models as M
from app.utils.security import decode_jwt
from app.exceptions.domain import (
    AuthenticationRequiredError,
    TokenExpiredError,
    InvalidTokenError,
    TokenDecodeError,
    PermissionDeniedError,
)


__all__ = [
    'CurrentUser',
    'CurrentOptionalUser',
    'require_scopes',
]


# OAuth2 scheme (API access via Bearer token)
access_token_scheme = OAuth2PasswordBearer(
    tokenUrl='/oauth2/token'
)


# Token-based authentication (OAuth2)
async def get_current_user_from_token(
    security_scopes: SecurityScopes,
    token: str = Depends(access_token_scheme),
    db: AsyncSession = Depends(get_db),
) -> M.User:

    try:
        payload = decode_jwt(token)

    except ExpiredSignatureError:
        raise TokenExpiredError()

    except JWTInvalidTokenError:
        raise InvalidTokenError()

    except DecodeError:
        raise TokenDecodeError()

    username = payload.get('sub')
    token_scopes = payload.get('scope', '').split()
    issuer = payload.get('iss')
    audience = payload.get('aud')

    if not username:
        raise InvalidTokenError()

    if issuer != "oauth-server":
        raise InvalidTokenError()

    if not audience:
        raise InvalidTokenError()

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise PermissionDeniedError(f"Missing scope: {scope}")

    db_user = await crud.get_user_by_username(
        username=username,
        db=db,
    )

    if not db_user:
        raise InvalidTokenError()

    if db_user.disabled:
        raise PermissionDeniedError("User disabled")

    return db_user


# Scope helper (clean usage in routes)
def require_scopes(*scopes: str):
    return Security(get_current_user_from_token, scopes=list(scopes))


# Cookie-based authentication (UI session)
async def _get_user_from_cookie_with_session(
    request: Request,
    db: AsyncSession,
) -> tuple[M.User, M.UserSession] | None:

    token = request.cookies.get("ui_access_token")

    if not token:
        return None

    db_session = await crud.get_session_by_session_id(db, token)

    if not db_session:
        return None

    db_user = await crud.get_user_by_id(db, db_session.user_id)

    if not db_user or db_user.disabled:
        return None

    await crud.update_session_activity(
        db,
        session_id=db_session.session_id,
    )

    return db_user, db_session


async def get_optional_user_from_cookie(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> M.User | None:

    result = await _get_user_from_cookie_with_session(request, db)

    if not result:
        return None

    db_user, _ = result
    return db_user


async def get_current_user_from_cookie(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> M.User:

    result = await _get_user_from_cookie_with_session(request, db)

    if not result:
        raise AuthenticationRequiredError()

    db_user, _ = result
    return db_user


CurrentUser = Annotated[M.User, Depends(get_current_user_from_cookie)]
CurrentOptionalUser = Annotated[M.User, Depends(get_optional_user_from_cookie)]
