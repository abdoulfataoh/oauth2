# coding: utf-8

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models as M


async def create_authorization_code(
    db: AsyncSession,
    *,
    code: str,
    client_id: str,
    user_id: str,
    redirect_uri: str,
    scopes: list[str],
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
    result = await db.execute(
        select(M.OAuthAuthorizationCode)
        .where(
            M.OAuthAuthorizationCode.code == code,
            M.OAuthAuthorizationCode.used.is_(False),
        )
    )
    db_code = result.scalars().first()

    if not db_code:
        return None

    db_code.used = True
    await db.commit()
    await db.refresh(db_code)
    return db_code


async def delete_expired_authorization_codes(
    db: AsyncSession,
    now: datetime,
) -> int:
    result = await db.execute(
        select(M.OAuthAuthorizationCode)
        .where(M.OAuthAuthorizationCode.expires_at < now)
    )

    codes = result.scalars().all()
    for code in codes:
        await db.delete(code)

    await db.commit()
    return len(codes)
