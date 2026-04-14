# coding: utf-8

from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from sqlalchemy.future import select

from app import models as M


async def create_authorization_code(
    db: AsyncSession,
    *,
    code: str,
    client_id: str,
    user_id: UUID,
    redirect_uri: str,
    scopes: list[str],
    state: str,
    code_challenge: str,
    code_challenge_method: str,
    expires_at: datetime,
) -> M.OAuthAuthorizationCode | None:

    db_code = M.OAuthAuthorizationCode(
        code=code,
        client_id=client_id,
        user_id=user_id,
        redirect_uri=redirect_uri,
        scopes=scopes,
        state=state,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        expires_at=expires_at,
    )

    db.add(db_code)
    await db.commit()
    await db.refresh(db_code)

    return db_code


async def get_authorization_code(
    db: AsyncSession,
    code: str,
) -> M.OAuthAuthorizationCode | None:

    result = await db.execute(
        select(M.OAuthAuthorizationCode)
        .where(M.OAuthAuthorizationCode.code == code)
    )

    return result.scalars().first()


async def mark_authorization_code_as_used(
    db: AsyncSession,
    *,
    code: str,
) -> M.OAuthAuthorizationCode | None:

    stmt = (
        update(M.OAuthAuthorizationCode)
        .where(
            M.OAuthAuthorizationCode.code == code,
            M.OAuthAuthorizationCode.used.is_(False),
        )
        .values(used=True)
        .returning(M.OAuthAuthorizationCode)
    )

    result = await db.execute(stmt)
    db_code = result.scalar_one_or_none()

    if not db_code:
        return None

    await db.commit()

    return db_code


async def delete_expired_authorization_codes(
    db: AsyncSession,
    *,
    now: datetime,
) -> int:
    result = await db.execute(
        delete(M.OAuthAuthorizationCode)
        .where(M.OAuthAuthorizationCode.expires_at < now)
    )

    await db.commit()

    return result.rowcount or 0  # type: ignore[attr-defined]
