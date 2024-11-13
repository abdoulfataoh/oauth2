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

from fastapi_oauth2_service import settings
from fastapi_oauth2_service import schemas
from fastapi_oauth2_service.security import create_access_token
from fastapi_oauth2_service.api import services
from fastapi_oauth2_service import crud
from fastapi_oauth2_service.db import get_db


__all__ = [
    'router',
]


def handle_fields_integrity_error(e: Exception) -> str:
    msg = str(e)
    issues_fields = []
    for field in 'email', 'username', 'phone_number':
        if f'auth_users.{field}' in msg:
            issues_fields.append(field)
    fields = ', '.join(issues_fields) or 'unknown'
    return f'Integrity error on fields: {fields}'


router = APIRouter()


@router.get('/oauth2/users', response_model=list[schemas.User])
async def get_users(db: AsyncSession = Depends(get_db)) -> list[schemas.User]:
    db_users = await crud.get_users(db=db)
    users_data = [schemas.User.model_validate(db_user) for db_user in db_users]
    return users_data


@router.get('/oauth2/user/{username}', response_model=schemas.User)
async def get_user_by_username(username: str, db: AsyncSession = Depends(get_db)) -> schemas.User:
    db_user = await crud.get_user_by_username(db=db, username=username)
    if db_user is None:
        raise HTTPException(status_code=400, detail='User not found')
    user_data = schemas.User.model_validate(db_user)
    return user_data


@router.post('/oauth2/user', response_model=schemas.User,)
async def add_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)) -> schemas.User:
    try:
        db_user = await crud.create_user(db=db, user=user)
        user_data = schemas.User.model_validate(db_user)
        return user_data
    except IntegrityError as e:
        issues_fields = handle_fields_integrity_error(e)
        raise HTTPException(status_code=400, detail=f'Integrity error on fields: {issues_fields}')


@router.delete('/oauth2/user/{user_id}')
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)) -> schemas.User:
    db_user = await crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail='User not found')
    user_data = schemas.User.model_validate(db_user)
    return user_data


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

    db_client = await crud.get_client(db=db, client_id=client_id)
    if not db_client:
        raise HTTPException(status_code=400, detail='Invalid client_id')

    client_data = schemas.Client.model_validate(db_client)
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
