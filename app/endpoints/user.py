# coding: utf-8

from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import Depends
from fastapi import APIRouter

from app.utils.exceptions import (
    ConflictedUserException, UserNotFoundException,
)
from app import schemas as S
from app import crud as CRUD
from app.db import get_db
from app.helpers._security import check_user


__all__ = [
    'router',
]


router = APIRouter()


@router.post('/oauth2/user', response_model=S.User,)
async def add_user(user: S.UserCreate, db: AsyncSession = Depends(get_db)) -> S.User:
    try:
        db_user = await CRUD.create_user(db=db, user=user)
        user_data = S.User.model_validate(db_user)
    except IntegrityError:
        raise ConflictedUserException
    return user_data


@router.get('/oauth2/users', response_model=list[S.User])
async def get_users(db: AsyncSession = Depends(get_db)) -> list[S.User]:
    db_users = await CRUD.get_users(db=db)
    users_data = [S.User.model_validate(db_user) for db_user in db_users]
    return users_data


@router.get('/oauth2/user/{username}', response_model=S.User)
async def get_user_by_username(username: str, db: AsyncSession = Depends(get_db)) -> S.User:
    db_user = await CRUD.get_user_by_username(db=db, username=username)
    if not db_user:
        raise UserNotFoundException
    user_data = S.User.model_validate(db_user)
    return user_data


@router.delete('/oauth2/user/{user_id}')
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)) -> S.User:
    db_user = await CRUD.delete_user(db=db, user_id=user_id)
    if not db_user:
        raise UserNotFoundException
    user_data = S.User.model_validate(db_user)
    return user_data


@router.post('oauth2/users/me')
async def me(
    current_user: Annotated[S.User, Depends(check_user)],
    db: AsyncSession = Depends(get_db),
) -> S.User:
    """
    Retrieve current user informations
    """
    return current_user
