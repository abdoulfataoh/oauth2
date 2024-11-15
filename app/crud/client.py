# coding: utf-8

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import schemas as S
from app import models as M
from app.utils.log import trace
from app.utils.security import Secret


__all__ = [
    'create_client', 'get_client', 'delete_client',
    'get_clients',
]


@trace
async def create_client(db: AsyncSession, client: S.ClientCreate) -> M.Client:
    """
    Create a new client application
    """
    client_secret = Secret.generate_secret(16)
    client_secret_hash = Secret.hash(client_secret)

    db_client = M.Client(
        client_name=client.client_name,
        redirect_uri=client.redirect_uri,
        client_id=Secret.generate_secret(16),
        client_secret=client_secret_hash
    )
    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    db_client.client_secret = client_secret
    return db_client


@trace
async def get_clients(db: AsyncSession, skip: int = 0, limit: int = 10) -> Sequence[M.Client]:
    """
    Retrieve all clients informations
    """
    result = await db.execute(select(M.Client).offset(skip).limit(limit))
    db_clients = result.scalars().all()
    return db_clients


@trace
async def get_client(db: AsyncSession, client_id: str) -> M.Client | None:
    """
    Retrieve an existing client informations by client_id
    """
    result = await db.execute(select(M.Client).where(M.Client.client_id == client_id))
    db_client = result.scalars().first()
    return db_client


@trace
async def delete_client(db: AsyncSession, client_id: int) -> M.Client | None:
    """
    Delete an existing client by client_id
    """
    result = await db.execute(select(M.Client).where(M.Client.client_id == client_id))
    db_client = result.scalars().first()
    if db_client:
        await db.delete(db_client)
        await db.commit()
        return db_client
    return None
