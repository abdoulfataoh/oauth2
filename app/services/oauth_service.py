# coding: utf-8

from datetime import timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import models as M

from app.utils.datetime import utcnow, is_expired
from app.utils.security import generate_secret, create_jwt
from app.utils.security import encode_base64, hash_sh256

from app.exceptions.domain import (
    ClientAuthenticationFailedError, InvalidClientRedirectURIError,
    AuthorizationRequestInvalidError, AuthorizationRequestExpiredError,
    AuthorizationRequestAlreadyBoundError, InvalidScopeError,
    InvalidCodeChallengeError, InvalidCodeChallengeMethodError,
    UnsupportedResponseTypeError,
)


async def request_authorize(
    *,
    client_id: str,
    redirect_uri: str,
    scopes: list[str],
    response_type: str,
    state: str,
    code_challenge: str,
    code_challenge_method: str = 'S256',
    expire_seconds: int,
    db: AsyncSession,
) -> M.OAuthAuthorizationRequest:

    if response_type != 'code':
        raise UnsupportedResponseTypeError()

    if not scopes:
        raise InvalidScopeError("At least one scope is required")

    if code_challenge_method != 'S256':
        raise InvalidCodeChallengeMethodError(
            "Only S256 code challenge method is supported"
        )

    if not code_challenge:
        raise InvalidCodeChallengeError("Code challenge is required")

    db_client = await crud.get_client_by_client_id(
        db=db,
        client_id=client_id,
    )

    if not db_client:
        raise ClientAuthenticationFailedError()

    if not all(scope in db_client.allowed_scopes for scope in scopes):
        raise InvalidScopeError(
            "One or more scopes are not allowed for this client"
        )

    if db_client.redirect_uri != redirect_uri:
        raise InvalidClientRedirectURIError()

    db_request = await crud.create_authorization_request(
        db=db,
        client_id=db_client.id,
        redirect_uri=redirect_uri,
        scopes=sorted(set(scopes)),
        state=state,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        expires_at=utcnow() + timedelta(
            seconds=expire_seconds,
        ),
    )

    return db_request


async def get_authorization_request_by_id(
    db: AsyncSession,
    request_id: UUID,
) -> M.OAuthAuthorizationRequest:

    db_request = await crud.get_authorization_request_by_id(
        db=db,
        request_id=request_id,
    )

    if not db_request:
        raise AuthorizationRequestInvalidError()
    
    if is_expired(db_request.expires_at):
        raise AuthorizationRequestExpiredError()

    return db_request


async def attach_user_to_request(
    request_id: UUID,
    user_id: UUID,
    db: AsyncSession,
) -> M.OAuthAuthorizationRequest:

    db_request = await get_authorization_request_by_id(
        db=db,
        request_id=request_id,
    )

    if db_request.user_id or db_request.approved:
        raise AuthorizationRequestAlreadyBoundError()

    db_request = await crud.attach_user_to_authorization_request(
        db=db,
        request_id=request_id,
        user_id=user_id,
    )

    if not db_request:
        raise AuthorizationRequestInvalidError()

    return db_request


async def approve_consent(
    request_id: UUID,
    user_id: UUID,
    approved: bool,
    expire_seconds: int,
    db: AsyncSession,
) -> M.OAuthAuthorizationCode:
    

    db_request = await get_authorization_request_by_id(
        db, request_id=request_id
    )

    if db_request.approved:
        raise AuthorizationRequestAlreadyBoundError()

    await crud.approve_authorization_request(
        db=db,
        request_id=request_id,
        approved=approved,
    )

    code = generate_secret(32)

    db_code = await crud.create_authorization_code(
        db=db,
        code=code,
        client_id=db_request.client_id,
        user_id=user_id,
        redirect_uri=db_request.redirect_uri,
        scopes=db_request.scopes,
        state=db_request.state,
        code_challenge=db_request.code_challenge,
        code_challenge_method=db_request.code_challenge_method,
        expires_at=utcnow() + timedelta(
            seconds=expire_seconds,
        ),
    )

    if not db_code:
        raise AuthorizationRequestInvalidError()

    return db_code


async def exchange_code2_token(
    user_id: UUID,
    client_id: UUID,
    authorization_id: UUID,

    grant_type: str,
    authorization_code: str,
    redirect_uri: str,
    code_verifier: str,
    expire_seconds: int,
    db: AsyncSession
):
    
    if grant_type != 'authorization_code':
        raise ...
        
    db_authorization_code = await crud.get_authorization_code(
        db=db,
        code=code_verifier
    )
    
    if not db_authorization_code:
        raise ...

    if not client_id == db_authorization_code.client_id:
        raise ...
    
    if not redirect_uri == db_authorization_code.redirect_uri:
        raise

    if is_expired(db_authorization_code.expires_at):
        raise ...
    
    code_verifier = encode_base64(hash_sh256(code_verifier))
    if not code_verifier == db_authorization_code.code_challenge:
        raise ...

    db_user = await crud.get_user_by_id(
        db=db,
        user_id=db_authorization_code.user_id
    )

    db_client = await crud.get_client_by_client_id(
        db=db,
        client_id=client_id
    )

    token = create_jwt(
        expires_in=expire_seconds,
        sub=db_user.username,
        iss='oauth server',
        aud=db_client.client_name,
    )

    return token
