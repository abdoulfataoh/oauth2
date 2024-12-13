# coding: utf-8

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import Depends
from fastapi import APIRouter

from app.utils.exceptions import (
    ClientNotFoundException, ConflictedClientException
)
from app import schemas as S
from app import crud as CRUD
from app.db import get_db
from app.settings import API_PREFIX


__all__ = [
    'router',
]


router = APIRouter()


@router.post(API_PREFIX + '/client', response_model=S.Client,)
async def add_client(client: S.ClientCreate, db: AsyncSession = Depends(get_db)) -> S.Client:
    try:
        db_client = await CRUD.create_client(db=db, client=client)
        client_data = S.Client.model_validate(db_client)
    except IntegrityError:
        raise ConflictedClientException
    return client_data


@router.get(API_PREFIX + '/clients', response_model=list[S.Client])
async def get_clients(db: AsyncSession = Depends(get_db)) -> list[S.Client]:
    db_clients = await CRUD.get_clients(db=db)
    clients_data = [S.Client.model_validate(db_client) for db_client in db_clients]
    return clients_data


@router.get(API_PREFIX + '/client/{client_id}', response_model=S.Client)
async def get_client(client_id: str, db: AsyncSession = Depends(get_db)) -> S.Client:
    db_client = await CRUD.get_client(db=db, client_id=client_id)
    if not db_client:
        raise ClientNotFoundException
    client_data = S.Client.model_validate(db_client)
    return client_data


@router.delete(API_PREFIX + '/client/{client_id}')
async def delete_client(client_id: str, db: AsyncSession = Depends(get_db)) -> S.Client:
    db_client = await CRUD.delete_client(db=db, client_id=client_id)
    if not db_client:
        raise ClientNotFoundException
    client_data = S.Client.model_validate(db_client)
    return client_data
