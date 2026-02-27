# coding: utf-8

from typing import AsyncGenerator, Any

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from app import settings

engine = create_async_engine(
    settings.DATABASE_URL,
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    async with SessionLocal() as session:
        yield session


class Base(DeclarativeBase):
    pass
