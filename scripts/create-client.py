# coding: utf-8

from pathlib import Path
import sys
import asyncio
import secrets

from sqlalchemy.ext.asyncio import AsyncSession

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir))

from app.db.sqlalchemy_manager import SessionLocal  # noqa: E402
from app import crud
from app.utils.security import hash_password


def generate_client_id() -> str:
    return secrets.token_urlsafe(32)


def generate_client_secret() -> str:
    return secrets.token_urlsafe(64)


async def create_client(db: AsyncSession):
    client_name = input('Project Name: ')
    redirect_uri = input('Project Redirect URI: ')
    allowed_scopes = input('Project Allowed Scopes (comma separated): ')

    client_id = generate_client_id()
    raw_client_secret = generate_client_secret()

    db_client = await crud.create_client(
        db,
        client_name=client_name,
        redirect_uri=redirect_uri,
        client_id=client_id,
        client_secret_hash=hash_password(raw_client_secret),
        allowed_scopes=[s.strip() for s in allowed_scopes.split(',')],
    )

    return db_client, raw_client_secret


async def main():
    async with SessionLocal() as db:
        client, raw_secret = await create_client(db)

        print('\nClient created successfully:')
        print(f'client_id={client.client_id}')
        print(f'client_secret={raw_secret}')


if __name__ == '__main__':
    asyncio.run(main())
