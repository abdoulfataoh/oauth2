# coding: utf-8

import os
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from start import app
from app.db import get_db, Base

TEST_DB_FILE = './test.db'
TEST_DB_URL = f'sqlite+aiosqlite:///{TEST_DB_FILE}'

engine = create_async_engine(
    TEST_DB_URL,
    connect_args={'check_same_thread': False},
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_db():
    from app import models

    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url='http://test'
    ) as ac:
        yield ac
