# coding: utf-8

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.security import AdminUser
from app import schemas as S
from app.db import get_db
from app import services

router = APIRouter()


@router.post('/client', response_model=S.Client, status_code=201)
async def add_client(
    client: S.ClientCreate,
    current_user: AdminUser,
    db: AsyncSession = Depends(get_db),
) -> S.Client:

    db_client, client_secret = await services.create_client(
        db,
        client,
    )

    response = S.Client.model_validate(db_client)

    response = response.model_copy(
        update={'client_secret': str(client_secret)},
    )

    return response


@router.get('/clients', response_model=list[S.Client])
async def get_clients(
    current_user: AdminUser,
    db: AsyncSession = Depends(get_db),
) -> list[S.Client]:

    clients = await services.get_clients(
        db,
    )

    return [
        S.Client.model_validate(c)
        for c in clients
    ]


@router.get('/client/{client_id}', response_model=S.Client)
async def get_client(
    client_id: UUID,
    current_user: AdminUser,
    db: AsyncSession = Depends(get_db),
) -> S.Client:

    db_client = await services.get_client_by_id(
        db,
        client_id,
    )

    return S.Client.model_validate(db_client)


@router.delete('/client/{client_id}', response_model=S.Client)
async def delete_client(
    client_id: UUID,
    current_user: AdminUser,
    db: AsyncSession = Depends(get_db),
) -> S.Client:

    db_client = await services.delete_client_by_id(
        db,
        client_id,
    )

    return S.Client.model_validate(db_client)
