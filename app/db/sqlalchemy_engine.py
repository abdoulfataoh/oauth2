# coding: utf-8

from sqlalchemy.ext.asyncio import create_async_engine

from app import settings


__all__ = [
    'engine',
]

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
)
