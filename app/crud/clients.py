# coding: utf-8

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models as M


async def create_client(
    db: AsyncSession,
    *,
    client_name: str,
    redirect_uri: str,
    client_id: str,
    client_secret_hash: str,
    allowed_scopes: list[str] | None = None,
) -> M.Client:
    db_client = M.Client(
        client_name=client_name,
        redirect_uri=redirect_uri,
        client_id=client_id,
        client_secret=client_secret_hash,
        allowed_scopes=allowed_scopes or [],
    )

    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    return db_client


async def get_clients(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
) -> Sequence[M.Client]:
    result = await db.execute(
        select(M.Client).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_client_by_client_id(
    db: AsyncSession,
    client_id: str,
) -> M.Client | None:
    result = await db.execute(
        select(M.Client).where(M.Client.client_id == client_id)
    )
    return result.scalars().first()


async def update_client_scopes(
    db: AsyncSession,
    *,
    client_id: str,
    allowed_scopes: list[str],
) -> M.Client | None:
    result = await db.execute(
        select(M.Client).where(M.Client.client_id == client_id)
    )
    db_client = result.scalars().first()

    if not db_client:
        return None

    db_client.allowed_scopes = allowed_scopes
    await db.commit()
    await db.refresh(db_client)
    return db_client


async def delete_client_by_client_id(
    db: AsyncSession,
    client_id: str,
) -> M.Client | None:
    result = await db.execute(
        select(M.Client).where(M.Client.client_id == client_id)
    )
    db_client = result.scalars().first()

    if not db_client:
        return None

    await db.delete(db_client)
    await db.commit()
    return db_client
