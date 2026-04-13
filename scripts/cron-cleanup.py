# coding: utf-8

import asyncio
from datetime import datetime
from pathlib import Path
import sys

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir))

from app.db.sqlalchemy_manager import SessionLocal  # noqa: E402
from app.crud import (
    delete_expired_authorization_requests,
    delete_expired_authorization_codes,
    delete_expired_otp,
)


def utcnow():
    return datetime.utcnow()


async def cleanup():
    now = utcnow()

    async with SessionLocal() as db:
        deleted_requests = await delete_expired_authorization_requests(
            db,
            now=now,
        )

        deleted_codes = await delete_expired_authorization_codes(
            db,
            now=now,
        )

        deleted_otps = await delete_expired_otp(
            db,
            now=now,
        )

        print("Cleanup done:")
        print(f"authorization_requests: {deleted_requests}")
        print(f"authorization_codes: {deleted_codes}")
        print(f"otps: {deleted_otps}")


if __name__ == "__main__":
    asyncio.run(cleanup())
