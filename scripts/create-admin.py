# coding: utf-8

from pathlib import Path
import sys
import asyncio
from getpass import getpass

from sqlalchemy.ext.asyncio import AsyncSession

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir))

from app.db.sqlalchemy_manager import SessionLocal
from app import crud
from app.utils.security import hash_password


async def create_admin(db: AsyncSession):
    username = input('Username: ')
    firstname = input('First name: ')
    lastname = input('Last name: ')
    email = input('Email (optional): ') or None
    phone = input('Phone (optional): ') or None
    password = getpass('Password: ')

    db_user = await crud.create_user(
        db,
        username=username,
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone=phone,
        password_hash=hash_password(password),
        roles=['admin'],
        verified=True,
        disabled=False,
    )

    return db_user


async def main():
    async with SessionLocal() as db:
        user = await create_admin(db)

        print('\nAdmin created successfully:')
        print(f'id={user.id}')
        print(f'username={user.username}')
        print(f'roles={user.roles}')


if __name__ == '__main__':
    asyncio.run(main())
