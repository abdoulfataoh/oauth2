# coding: utf-8

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import models as M


async def create_session(
    db: AsyncSession,
    *,
    user_id: UUID,
    user_agent: str,
    ip_address: str,
    device_type: str,
    device_name: str,
    browser: str,
    os: str,
    location: str | None = None,
) -> M.UserSession:

    db_session = await crud.create_session(
        db,
        user_id=user_id,
        device_type=device_type,
        device_name=device_name,
        browser=browser,
        os=os,
        ip_address=ip_address,
        user_agent=user_agent,
        location=location,
    )

    return db_session


async def get_my_sessions(
    db: AsyncSession,
    user_id: UUID,
) -> list[M.UserSession]:

    sessions = await crud.get_sessions_by_user_id(
        db,
        user_id,
    )

    return list(sessions)


async def refresh_session_activity(
    db: AsyncSession,
    session_id: str,
) -> M.UserSession | None:

    return await crud.update_session_activity(
        db,
        session_id=session_id,
    )


async def logout_session(
    db: AsyncSession,
    session_id: str,
) -> M.UserSession | None:

    session = await crud.deactivate_session(
        db,
        session_id,
    )

    if not session:
        return None

    return session


async def logout_all_sessions(
    db: AsyncSession,
    user_id: UUID,
) -> int:

    return await crud.delete_sessions_by_user_id(
        db,
        user_id,
    )


async def delete_session(
    db: AsyncSession,
    session_id: str,
) -> M.UserSession | None:

    return await crud.delete_session_by_id(
        db,
        session_id,
    )
