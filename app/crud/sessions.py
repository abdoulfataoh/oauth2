# coding: utf-8

from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models as M
from app.utils.datetime import utcnow


async def create_session(
    db: AsyncSession,
    *,
    user_id: UUID,
    device_type: str,
    device_name: str,
    browser: str,
    os: str,
    ip_address: str,
    user_agent: str,
    location: str | None = None,
) -> M.UserSession:

    db_session = M.UserSession(
        user_id=user_id,
        device_type=device_type,
        device_name=device_name,
        browser=browser,
        os=os,
        ip_address=ip_address,
        user_agent=user_agent,
        location=location,
    )

    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)

    return db_session


async def get_sessions_by_user_id(
    db: AsyncSession,
    user_id: UUID,
) -> Sequence[M.UserSession]:

    result = await db.execute(
        select(M.UserSession)
        .where(M.UserSession.user_id == user_id)
        .order_by(M.UserSession.last_activity.desc())
    )

    return result.scalars().all()


async def get_session_by_session_id(
    db: AsyncSession,
    session_id: str,
) -> M.UserSession | None:

    result = await db.execute(
        select(M.UserSession).where(M.UserSession.session_id == session_id)
    )

    return result.scalars().first()


async def update_session_activity(
    db: AsyncSession,
    *,
    session_id: str,
) -> M.UserSession | None:

    result = await db.execute(
        select(M.UserSession).where(M.UserSession.session_id == session_id)
    )

    db_session = result.scalars().first()

    if not db_session:
        return None

    db_session.last_activity = utcnow()

    await db.commit()
    await db.refresh(db_session)

    return db_session


async def deactivate_session(
    db: AsyncSession,
    session_id: str,
) -> M.UserSession | None:

    result = await db.execute(
        select(M.UserSession).where(M.UserSession.session_id == session_id)
    )

    db_session = result.scalars().first()

    if not db_session:
        return None

    db_session.is_active = False

    await db.commit()
    await db.refresh(db_session)

    return db_session


async def delete_session_by_id(
    db: AsyncSession,
    session_id: str,
) -> M.UserSession | None:

    result = await db.execute(
        select(M.UserSession).where(M.UserSession.id == session_id)
    )

    db_session = result.scalars().first()

    if not db_session:
        return None

    await db.delete(db_session)
    await db.commit()

    return db_session


async def delete_sessions_by_user_id(
    db: AsyncSession,
    user_id: UUID,
) -> int:

    result = await db.execute(
        select(M.UserSession).where(M.UserSession.user_id == user_id)
    )

    sessions = result.scalars().all()

    count = len(sessions)

    for session in sessions:
        await db.delete(session)

    await db.commit()

    return count
