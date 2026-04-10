# coding: utf-8

from typing import Annotated

from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app import crud
from app import models as M
from app.exceptions.domain import AuthenticationRequiredError


__all__ = [
    'CurrentUser',
    'CurrentOptionalUser',
]


async def _get_user_from_cookie_with_session(
    request: Request,
    db: AsyncSession,
) -> tuple[M.User, M.UserSession] | None:

    token = request.cookies.get('ui_access_token')

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

    result = await _get_user_from_cookie_with_session(
        request,
        db,
    )

    if not result:
        return None

    db_user, _ = result
    return db_user


async def get_current_user_from_cookie(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> M.User:

    result = await _get_user_from_cookie_with_session(
        request,
        db,
    )

    if not result:
        raise AuthenticationRequiredError()

    db_user, _ = result
    return db_user


CurrentUser = Annotated[M.User, Depends(get_current_user_from_cookie)]
CurrentOptionalUser = Annotated[M.User, Depends(get_optional_user_from_cookie)]
