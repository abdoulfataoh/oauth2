# coding: utf-8
# Copyright (C) 2024 vela

from pathlib import Path
import sys
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

base_dir = Path(__file__).resolve().parent.parent
app_dir = base_dir
sys.path.insert(0, str(app_dir))

from fastapi_oauth2_service.db import get_db  # noqa: E402
from fastapi_oauth2_service.models import Client as ClientModel  # noqa: E402
from fastapi_oauth2_service.schemas import ClientCreate as ClientCreateSchemas  # noqa: E402


async def create_client(db: AsyncSession):
    client_name = input("Project Name: ")
    redirect_uri = input("Project Redirect URI: ")
    client = ClientCreateSchemas(
        client_name=client_name,
        redirect_uri=redirect_uri
    )
    db_client = ClientModel(**client.__dict__)
    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    return db_client


async def main():
    async for db in get_db():
        db_client = await create_client(db)
        client_id = db_client.client_id
        client_secret = db_client.client_secret
        print(f"{client_id=}\n{client_secret=}")


if __name__ == "__main__":
    asyncio.run(main())
