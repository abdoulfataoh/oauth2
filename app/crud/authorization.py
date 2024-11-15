# coding: utf-8

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import schemas as S
from app import models as M
from app.utils.log import trace


__all__ = [
    'create_authorization', 'update_authorization',
    'delete_authorization', 'get_authorizations_by_user_id',
]


@trace
async def create_authorization(
    db: AsyncSession, authorization: S.AuthorizationCreate
) -> M.Authorization:
    db_authorization = M.Authorization(**authorization.model_dump())
    db.add(db_authorization)
    await db.commit()
    await db.refresh(db_authorization)
    return db_authorization


@trace
async def update_authorization(
    db: AsyncSession,
    authorization_id: str,
    authorization: S.AuthorizationCreate
) -> M.Authorization:

    result = await db.execute(select(M.Authorization).where(M.Authorization.id == authorization_id))
    db_authorization = result.scalars().first()

    if db_authorization:
        for key, value in vars(authorization).items():
            setattr(db_authorization, key, value)
        await db.commit()
        await db.refresh(db_authorization)
        return db_authorization
    return None


@trace
async def delete_authorization(db: AsyncSession, authorization_id: int) -> M.Authorization | None:
    result = await db.execute(select(M.Authorization).where(M.Authorization.id == authorization_id))
    db_authorization = result.scalars().first()
    if db_authorization:
        await db.delete(db_authorization)
        await db.commit()
        return db_authorization
    return None


@trace
async def get_authorizations_by_user_id(db: AsyncSession, user_id: str) -> Sequence[M.Authorization]:
    result = await db.execute(select(M.Authorization).where(M.Authorization.user_id == user_id))
    db_authorizations = result.scalars().all()
    return db_authorizations
