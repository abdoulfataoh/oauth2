# coding: utf-8

from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app import crud
from app import schemas as S
from app import models as M
from app.utils.security import generate_secret, hash_password
from app.utils.exceptions import (
    ConflictedClientException,
    InvalidFieldsException,
    ClientNotFoundException,
)


async def create_client_service(
    db: AsyncSession,
    client: S.ClientCreate,
) -> tuple[M.Client, str]:
    client_id = str(uuid4().hex).upper()
    client_secret = generate_secret(32)
    client_secret_hash = hash_password(client_secret)

    try:
        db_client = await crud.create_client(
            db,
            client_name=client.client_name,
            redirect_uri=client.redirect_uri,
            client_id=client_id,
            client_secret_hash=client_secret_hash,
            allowed_scopes=client.allowed_scopes,
        )
    except IntegrityError as e:
        msg = str(e.orig).lower()

        if 'unique' in msg:
            raise ConflictedClientException()
        if 'not null' in msg:
            raise InvalidFieldsException("Missing required field")
        raise

    return db_client, client_secret


async def get_clients_service(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
) -> list[M.Client]:
    return list(await crud.get_clients(db, skip, limit))


async def get_client_by_client_id_service(
    db: AsyncSession,
    client_id: str,
) -> M.Client:
    db_client = await crud.get_client_by_client_id(db, client_id)

    if not db_client:
        raise ClientNotFoundException

    return db_client


async def delete_client_by_client_id_service(
    db: AsyncSession,
    client_id: str,
) -> M.Client:
    db_client = await crud.delete_client_by_client_id(db, client_id)

    if not db_client:
        raise ClientNotFoundException

    return db_client
