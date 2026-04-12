# coding: utf-8

from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models as M


async def create_authorization_request(
    db: AsyncSession,
    *,
    client_id: str,
    redirect_uri: str,
    scopes: list[str],
    state: str,
    code_challenge: str,
    code_challenge_method: str,
    expires_at: datetime,
) -> M.OAuthAuthorizationRequest:
    '''
    Create a new OAuth authorization request.
    '''

    db_request = M.OAuthAuthorizationRequest(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scopes=scopes,
        state=state,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        expires_at=expires_at,
        user_id=None,
        approved=None,
    )

    db.add(db_request)
    await db.commit()
    await db.refresh(db_request)

    return db_request


async def get_authorization_request_by_id(
    db: AsyncSession,
    request_id: UUID,
) -> M.OAuthAuthorizationRequest | None:
    '''
    Fetch an authorization request by its ID.
    '''

    result = await db.execute(
        select(M.OAuthAuthorizationRequest)
        .where(M.OAuthAuthorizationRequest.id == request_id)
    )

    return result.scalars().first()


async def attach_user_to_authorization_request(
    db: AsyncSession,
    *,
    request_id: UUID,
    user_id: UUID,
) -> M.OAuthAuthorizationRequest | None:
    '''
    Attach an authenticated user to an authorization request.
    '''

    result = await db.execute(
        select(M.OAuthAuthorizationRequest)
        .where(M.OAuthAuthorizationRequest.id == request_id)
    )

    db_request = result.scalars().first()

    if not db_request:
        return None

    db_request.user_id = user_id

    await db.commit()
    await db.refresh(db_request)

    return db_request


async def approve_authorization_request(
    db: AsyncSession,
    *,
    request_id: UUID,
    approved: bool,
) -> M.OAuthAuthorizationRequest | None:
    '''
    Approve or deny an authorization request.
    '''

    result = await db.execute(
        select(M.OAuthAuthorizationRequest)
        .where(M.OAuthAuthorizationRequest.id == request_id)
    )

    db_request = result.scalars().first()

    if not db_request:
        return None

    db_request.approved = approved

    await db.commit()
    await db.refresh(db_request)

    return db_request


async def delete_expired_authorization_requests(
    db: AsyncSession,
    *,
    now: datetime,
) -> int:
    '''
    Delete all expired authorization requests.
    '''

    result = await db.execute(
        delete(M.OAuthAuthorizationRequest)
        .where(M.OAuthAuthorizationRequest.expires_at < now)
    )

    await db.commit()

    return result.rowcount or 0  # type: ignore[attr-defined]
