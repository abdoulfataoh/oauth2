# coding: utf-8

from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app import settings
from app.utils.exceptions import LoginFailedException
from app.utils.security import create_jwt
from app import schemas as S
from app import crud as CRUD
from app.db import get_db


__all__ = [
    'router',
]


router = APIRouter()


@router.post('/oauth2/token')
async def login(
    login_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
) -> S.Token:
    """
    Login for token
    """
    # Auth user
    db_user = await CRUD.authenticate_user(
        db=db, username=login_form.username, password=login_form.password
    )
    if not db_user:
        raise LoginFailedException

    token_expire = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    token = create_jwt(user_id=db_user.id, expires_in=token_expire)
    return S.Token(access_token=token, token_type='bearer')
