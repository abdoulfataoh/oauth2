# coding: utf-8

from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from app import models as M


async def create_otp(
    db: AsyncSession,
    *,
    user_id: UUID,
    recipient: str,
    code: str,
    otp_type: str,
    channel: str,
    expires_at: datetime,
) -> M.Otp:

    db_otp = M.Otp(
        user_id=user_id,
        recipient=recipient,
        code=code,
        otp_type=otp_type,
        channel=channel,
        expires_at=expires_at,
    )

    db.add(db_otp)
    await db.commit()
    await db.refresh(db_otp)

    return db_otp


async def get_otp(
    db: AsyncSession,
    *,
    user_id: UUID,
    recipient: str,
    otp_type: str,
    channel: str,

) -> M.Otp | None:

    result = await db.execute(
        select(M.Otp).where(
            M.Otp.recipient == recipient,
            M.Otp.otp_type == otp_type,
            M.Otp.channel == channel,
            M.Otp.user_id == user_id
        )
    )

    return result.scalars().first()


async def increment_otp_attempts(
    db: AsyncSession,
    otp_id: UUID,
) -> M.Otp | None:

    result = await db.execute(
        select(M.Otp).where(
            M.Otp.id == otp_id
        )
    )

    db_otp = result.scalars().first()

    if not db_otp:
        return None

    db_otp.attempts += 1

    await db.commit()
    await db.refresh(db_otp)

    return db_otp


async def delete_otp(
    db: AsyncSession,
    otp_id: UUID,
) -> None:

    result = await db.execute(
        select(M.Otp).where(
            M.Otp.id == otp_id
        )
    )

    db_otp = result.scalars().first()

    if db_otp:
        await db.delete(db_otp)
        await db.commit()


async def delete_expired_otp(
    db: AsyncSession,
    *,
    now: datetime,
) -> int:
    result = await db.execute(
        delete(M.Otp)
        .where(M.Otp.expires_at < now)
    )

    await db.commit()

    return result.rowcount or 0  # type: ignore[attr-defined]
