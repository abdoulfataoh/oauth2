# coding: utf-8

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi_oauth2_service.schemas import UserBase as UserBaseSchemas
from fastapi_oauth2_service.schemas import UserCreate as UserCreateSchemas
from fastapi_oauth2_service.models import User as UserModel
from fastapi_oauth2_service.security import secret
from fastapi_oauth2_service.traces import trace_call


__all__ = [
    'create_user',
    'update_user',
    'get_user',
    'get_user_by_username',
    'get_users',
    'delete_user',
]


@trace_call
async def create_user(db: AsyncSession, user: UserCreateSchemas) -> UserModel:
    hashed_password = secret.hash(user.password.get_secret_value())
    db_user = UserModel(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        phone_number=user.phone_number,
        disabled=True,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@trace_call
async def update_user(db: AsyncSession, user: UserBaseSchemas, user_id: str) -> UserModel | None:
    result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
    db_user = result.scalars().first()
    if db_user:
        for key, value in vars(user).items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    return None


@trace_call
async def get_user(db: AsyncSession, user_id: str) -> UserModel | None:
    result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
    db_user = result.scalars().first()
    return db_user


@trace_call
async def get_user_by_username(db: AsyncSession, username: str) -> UserModel | None:
    result = await db.execute(select(UserModel).filter(UserModel.username == username))
    db_user = result.scalars().first()
    return db_user


@trace_call
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10) -> Sequence[UserModel]:
    result = await db.execute(select(UserModel).offset(skip).limit(limit))
    db_users = result.scalars().all()
    return db_users


@trace_call
async def delete_user(db: AsyncSession, user_id: int) -> UserModel | None:
    result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
    db_user = result.scalars().first()
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return db_user
    return None
