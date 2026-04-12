# coding: utf-8

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app import crud
from app import schemas as S
from app import models as M
from app.utils.security import generate_secret, hash_password

from app.exceptions.domain import (
    ClientAlreadyExistsError, ClientNotFoundError, InvalidFieldsError,
)


async def create_client(
    db: AsyncSession,
    client: S.ClientCreate,
) -> tuple[M.Client, str]:

    client_id = 'app.' + generate_secret(32)

    client_secret = generate_secret(32)
    client_secret_hash = hash_password(client_secret)

    try:
        db_client = await crud.create_client(
            db=db,
            client_name=client.client_name,
            redirect_uri=client.redirect_uri,
            client_id=client_id,
            client_secret_hash=client_secret_hash,
            allowed_scopes=client.allowed_scopes,
        )

    except IntegrityError as e:
        msg = str(e.orig).lower()

        if 'unique' in msg:
            raise ClientAlreadyExistsError()

        if 'not null' in msg:
            raise InvalidFieldsError("Missing required field")

        raise

    return db_client, client_secret


async def get_clients(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
) -> list[M.Client]:

    clients = await crud.get_clients(
        db=db,
        skip=skip,
        limit=limit,
    )

    return list(clients)


async def get_client_by_client_id(
    db: AsyncSession,
    client_id: str,
) -> M.Client:

    db_client = await crud.get_client_by_client_id(
        db=db,
        client_id=client_id,
    )

    if not db_client:
        raise ClientNotFoundError()

    return db_client


async def get_client_by_id(
    db: AsyncSession,
    client_id: UUID,
) -> M.Client:

    db_client = await crud.get_client_by_id(
        db=db,
        client_id=client_id,
    )

    if not db_client:
        raise ClientNotFoundError()

    return db_client


async def delete_client_by_id(
    db: AsyncSession,
    client_id: UUID,
) -> M.Client:

    db_client = await crud.delete_client_by_id(
        db=db,
        client_id=client_id,
    )

    if not db_client:
        raise ClientNotFoundError()

    return db_client
