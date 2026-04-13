# coding: utf-8

import asyncio

from app.db import engine
from app.db import Base

from app import models


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(create_tables())
