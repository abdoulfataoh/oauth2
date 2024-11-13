# coding: utf-8

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Authorization as AuthorizationModel
from app.schemas import AuthorizationCreate
from app.traces import trace_call


__all__ = [
    'create_authorization',
    'update_authorization',
    'delete_authorization',
    'get_authorizations_by_user_id',
]


@trace_call
async def create_authorization(
    db: AsyncSession,
    authorization: AuthorizationCreate
) -> AuthorizationModel:

    db_authorization = AuthorizationModel(**authorization.model_dump())
    db.add(db_authorization)
    await db.commit()
    await db.refresh(db_authorization)
    return db_authorization


@trace_call
async def update_authorization(
    db: AsyncSession,
    authorization_id: str,
    authorization: AuthorizationCreate
) -> AuthorizationModel:

    result = await db.execute(select(AuthorizationModel).where(AuthorizationModel.id == authorization_id))
    db_authorization = result.scalars().first()

    if db_authorization:
        for key, value in vars(authorization).items():
            setattr(db_authorization, key, value)
        await db.commit()
        await db.refresh(db_authorization)
        return db_authorization
    return None


@trace_call
async def delete_authorization(db: AsyncSession, authorization_id: int) -> AuthorizationModel | None:
    result = await db.execute(select(AuthorizationModel).where(AuthorizationModel.id == authorization_id))
    db_authorization = result.scalars().first()
    if db_authorization:
        await db.delete(db_authorization)
        await db.commit()
        return db_authorization
    return None


@trace_call
async def get_authorizations_by_user_id(db: AsyncSession, user_id: str) -> Sequence[AuthorizationModel]:
    result = await db.execute(select(AuthorizationModel).where(AuthorizationModel.user_id == user_id))
    db_authorizations = result.scalars().all()
    return db_authorizations
