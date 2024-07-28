# coding: utf-8

from typing import AsyncGenerator
from typing import Any

from sqlalchemy.orm import sessionmaker

from fastapi_oauth2_service.db.sqlalchemy_engine import engine
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = [
    'SessionLocal',
    'get_db',
]

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)  # type: ignore


async def get_db() -> AsyncGenerator[Any, Any]:
    async with SessionLocal() as session:
        yield session
