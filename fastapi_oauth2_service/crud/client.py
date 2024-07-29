# coding: utf-8

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi_oauth2_service.models import Client as ClientModel
from fastapi_oauth2_service.traces.function_trace import trace_call


__all__ = [
    'get_client',
]


@trace_call
async def get_client(db: AsyncSession, client_id: str) -> ClientModel | None:
    result = await db.execute(select(ClientModel).filter(ClientModel.client_id == client_id))
    db_client = result.scalars().first()
    return db_client
