# coding: utf-8

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models as M


async def create_user(
    db: AsyncSession,
    *,
    username: str, firstname: str, lastname: str, email: str,
    phone: str | None, password_hash: str, disabled: bool, roles: list[str]
) -> M.User:
    db_user = M.User(
        username=username, firstname=firstname, lastname=lastname,
        email=email, phone=phone, roles=roles, disabled=disabled,
        password_hash=password_hash,
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user_by_id(
    db: AsyncSession,
    user_id: str,
    data: dict,
) -> M.User | None:
    result = await db.execute(
        select(M.User).where(M.User.id == user_id)
    )
    db_user = result.scalars().first()

    if not db_user:
        return None

    for key, value in data.items():
        setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_id(
    db: AsyncSession,
    user_id: str,
) -> M.User | None:
    result = await db.execute(
        select(M.User).where(M.User.id == user_id)
    )
    return result.scalars().first()


async def get_user_by_username(
    db: AsyncSession,
    username: str,
) -> M.User | None:
    result = await db.execute(
        select(M.User).where(M.User.username == username)
    )
    return result.scalars().first()


async def get_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
) -> Sequence[M.User]:
    result = await db.execute(
        select(M.User).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def delete_user_by_id(
    db: AsyncSession,
    user_id: str,
) -> M.User | None:
    result = await db.execute(
        select(M.User).where(M.User.id == user_id)
    )
    db_user = result.scalars().first()

    if not db_user:
        return None

    await db.delete(db_user)
    await db.commit()
    return db_user


async def update_user_password(
    db: AsyncSession,
    user_id: str,
    password_hash: str,
) -> M.User | None:
    result = await db.execute(
        select(M.User).where(M.User.id == user_id)
    )
    db_user = result.scalars().first()

    if not db_user:
        return None

    db_user.password_hash = password_hash
    await db.commit()
    await db.refresh(db_user)
    return db_user
