# coding: utf-8

from pathlib import Path
import sys
import asyncio
from datetime import datetime, date
import getpass

from sqlalchemy.ext.asyncio import AsyncSession

# --- setup path ---
base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir))

# --- imports app ---
from app.db import get_db  # noqa: E402
from app.services import create_user  # noqa: E402


# --- helper DB ---
async def get_db_session() -> AsyncSession:
    async for db in get_db():
        return db


# --- parse date ---
def parse_birthdate(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Format attendu: YYYY-MM-DD")


# --- main ---
async def create_admin():
    print('*' * 5)
    print("Create Admin User\n")

    username = input("Username: ")
    firstname = input("Firstname: ")
    lastname = input("Lastname: ")
    email = input("Email: ")
    phone = input("Phone: ")

    birthdate_input = input("Birthdate (YYYY-MM-DD): ")
    birthdate = parse_birthdate(birthdate_input)

    password = getpass.getpass("Password: ")

    disabled = False
    verified = True
    roles = ['admin']

    db = await get_db_session()

    user = await create_user(
        db=db,
        username=username,
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone=phone,
        birthdate=birthdate,  # ✅ objet date
        password=password,
        disabled=disabled,
        verified=verified,
        roles=roles,
    )

    print("\n✅ Admin created successfully")
    print(f"ID: {user.id}")
    print(f"Username: {user.username}")

    return user


# --- entrypoint ---
if __name__ == '__main__':
    asyncio.run(create_admin())
