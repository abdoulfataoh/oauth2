# coding: utf-8

import uuid
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.utils.log import trace
from app import models as M


__all__ = [
    'create_session', 'get_session',
]


@trace
async def create_session(db: AsyncSession, username: str) -> M.Session:
    session_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=1)
    db_session = M.Session(
        session_id=session_id, username=username,
        expires_at=expires_at
    )
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)
    return db_session


@trace
async def get_session(db: AsyncSession, session_id: str) -> M.Session | None:
    """
    Retrieve an existing session
    """
    result = await db.execute(select(M.Session).where(M.Session.session_id == session_id))
    db_session = result.scalars().first()
    return db_session
