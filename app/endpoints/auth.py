# coding: utf-8

import secrets
from datetime import timedelta
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter

from app.utils.exceptions import (
    ConflictedUserException, UserNotFoundException,
)
from app import settings
from app import schemas as S
from app.utils.security import Secret
from app import crud as CRUD
from app.db import get_db


__all__ = [
    'router',
]


router = APIRouter()

@router.get('/oauth2/authorize')
async def authorize(
    response_type: str,
    client_id: str,
    redirect_uri: str,
    scope: str,
    db: AsyncSession = Depends(get_db)
) -> RedirectResponse:
    del scope  # todo
    if response_type != 'code':
        raise HTTPException(status_code=400, detail='Unsupported response_type')

    db_client = await CRUD.get_client(db=db, client_id=client_id)
    if not db_client:
        raise HTTPException(status_code=400, detail='Invalid client_id')

    client_data = S.Client.model_validate(db_client)
    if client_data.redirect_uri != redirect_uri:
        raise HTTPException(status_code=400, detail='Invalid redirect_uri')

    authorization_code = 'AUTH_CODE_' + secrets.token_urlsafe(16)
    auth_codes_db = {}
    auth_codes_db[authorization_code] = {
        'client_id': client_id,
    }

    redirect_url = f'{redirect_uri}?code={authorization_code}'
    return RedirectResponse(url=redirect_url)


@router.post('/oauth2/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db)
) -> schemas.Token:

    user = services.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expire_minutes = settings.OAUTH2_ACCESS_TOKEN_EXPIRE_MINUTES
    access_token_expires = timedelta(minutes=access_token_expire_minutes)
    access_token = create_access_token(
        data={'sub': user.username},  # type: ignore
        expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type='bearer')
