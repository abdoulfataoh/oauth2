# coding: utf-8

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_oauth2_service.security import secret

from fastapi_oauth2_service.schemas import User as UserSchemas
from fastapi_oauth2_service import crud
from fastapi_oauth2_service.traces import trace_call


@trace_call
async def authenticate_user(db: AsyncSession, username: str, password: str) -> bool | UserSchemas:
    db_user = await crud.get_user_by_username(db, username)
    if not db_user:
        return False
    user_model = UserSchemas.model_validate(db_user)
    if not secret.verify(password, db_user.hashed_password):
        return False
    return user_model


@trace_call
async def change_user_password(db: AsyncSession, username: str, password: str) -> bool | UserSchemas:
    db_user = await crud.get_user_by_username(db, username)
    if not db_user:
        return False
    user_model = UserSchemas.model_validate(db_user)
    if not secret.verify(password, db_user.hashed_password):
        return False
    return user_model
