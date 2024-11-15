# coding: utf-8

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.utils.log import trace
from app import schemas as S
from app import models as M
from app.utils.security import Secret, generate_username


__all__ = [
    'create_user', 'update_user', 'get_user',
    'get_user_by_username', 'get_users', 'delete_user',
]


@trace
async def create_user(db: AsyncSession, user: S.UserCreate) -> M.User:
    """
    Create a new user in DB
    """
    password_hash = Secret.hash(user.password.get_secret_value())
    username = generate_username(
        user.firstname, user.lastname, user.phone_number
    )
    db_user = M.User(
        username=username, firstname=user.firstname, lastname=user.lastname,
        email=user.email, phone_number=user.phone_number,
        disabled=True, password_hash=password_hash,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@trace
async def update_user(db: AsyncSession, user: S.UserBase, user_id: str) -> M.User | None:
    """
    Update existing user base informations
    """
    result = await db.execute(select(M.User).where(M.User.id == user_id))
    db_user = result.scalars().first()
    if db_user:
        for key, value in vars(user).items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    return None


@trace
async def get_user(db: AsyncSession, user_id: str) -> M.User | None:
    """
    Retrieve an existing user informations by id
    """
    result = await db.execute(select(M.User).where(M.User.id == user_id))
    db_user = result.scalars().first()
    return db_user


@trace
async def get_user_by_username(db: AsyncSession, username: str) -> M.User | None:
    """
    Retrieve an existing user informations by username
    """
    result = await db.execute(select(M.User).where(M.User.username == username))
    db_user = result.scalars().first()
    return db_user


@trace
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10) -> Sequence[M.User]:
    """
    Retrieve all users informations
    """
    result = await db.execute(select(M.User).offset(skip).limit(limit))
    db_users = result.scalars().all()
    return db_users


@trace
async def delete_user(db: AsyncSession, user_id: int) -> M.User | None:
    """
    Delete an existing user by user_id
    """
    result = await db.execute(select(M.User).where(M.User.id == user_id))
    db_user = result.scalars().first()
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return db_user
    return None


@trace
async def authenticate_user(db: AsyncSession, username: str, password: str) -> bool | S.User:
    """
    Auth user by username and password
    """
    db_user = await get_user_by_username(db, username)
    if not db_user:
        return False
    user_model = S.User.model_validate(db_user)
    if not Secret.verify(password, db_user.password_hash):
        return False
    return user_model


@trace
async def change_user_password(db: AsyncSession, username: str, password: str) -> bool | S.User:
    """
    Change an existing user password
    """
    db_user = await get_user_by_username(db, username)
    if not db_user:
        return False
    user_model = S.User.model_validate(db_user)
    if not Secret.verify(password, db_user.password_hash):
        return False
    return user_model
