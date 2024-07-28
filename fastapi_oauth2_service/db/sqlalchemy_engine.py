# coding: utf-8

from sqlalchemy.ext.asyncio import create_async_engine

from fastapi_oauth2_service import settings


__all__ = [
    'engine',
]

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
)
