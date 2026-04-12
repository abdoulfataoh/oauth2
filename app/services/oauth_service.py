# coding: utf-8

import logging
from datetime import timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import models as M

from app.utils.datetime import utcnow, is_expired
from app.utils.security import generate_secret, create_jwt
from app.utils.security import encode_base64, hash_sha256

from app.exceptions.domain import (
    ClientAuthenticationFailedError, InvalidClientRedirectURIError,
    AuthorizationRequestInvalidError, AuthorizationRequestExpiredError,
    AuthorizationRequestAlreadyBoundError, InvalidScopeError,
    InvalidCodeChallengeError, InvalidCodeChallengeMethodError,
    UnsupportedResponseTypeError, UnsupportedGrantTypeError, InvalidAuthorizationCodeError,
    UserNotFoundError, ClientNotFoundError, PermissionDeniedError
)


logger = logging.getLogger(__name__)


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

    if not (43 <= len(code_challenge) <= 128):
        raise InvalidCodeChallengeError("Code challenge with length >=43 & <=128 is required")

    if not scopes:
        raise InvalidScopeError("At least one scope is required")

    if code_challenge_method != 'S256':
        raise InvalidCodeChallengeMethodError(
            "Only S256 code challenge method is supported"
        )

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
        client_id=db_client.client_id,
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

    if not db_request:
        raise AuthorizationRequestInvalidError()

    if db_request.user_id is not None:
        raise AuthorizationRequestAlreadyBoundError()

    await crud.attach_user_to_authorization_request(
        db=db,
        request_id=request_id,
        user_id=user_id,
    )

    return db_request


async def approve_consent(
    request_id: UUID,
    user_id: UUID,
    approved: bool,
    expire_seconds: int,
    db: AsyncSession,
) -> M.OAuthAuthorizationCode | None:

    db_request = await get_authorization_request_by_id(
        db, request_id=request_id
    )

    if db_request.approved is not None:
        raise AuthorizationRequestAlreadyBoundError()

    if user_id != db_request.user_id:
        raise PermissionDeniedError()

    await crud.approve_authorization_request(
        db=db,
        request_id=request_id,
        approved=approved,
    )

    if approved:

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
    return None


async def exchange_code_to_token(
    client_id: str,
    grant_type: str,
    authorization_code: str,
    redirect_uri: str,
    code_verifier: str,
    expire_seconds: int,
    db: AsyncSession
):

    if grant_type != 'authorization_code':
        raise UnsupportedGrantTypeError(
            "Invalid grant_type, only 'authorization_code' supported."
        )

    if not (43 <= len(code_verifier) <= 128):
        logger.warning("Invalid code_verifier length")
        raise InvalidAuthorizationCodeError()

    db_authorization_code = await crud.mark_authorization_code_as_used(
        db=db,
        code=authorization_code,
    )

    if not db_authorization_code:
        logger.warning("Authorization code invalid or already used")
        raise InvalidAuthorizationCodeError()

    if is_expired(db_authorization_code.expires_at):
        logger.warning("Authorization code expired")
        raise InvalidAuthorizationCodeError()

    if client_id != db_authorization_code.client_id:
        logger.warning("Client authentication failed")
        raise InvalidAuthorizationCodeError()

    if redirect_uri != db_authorization_code.redirect_uri:
        logger.warning("Invalid client redirect URI")
        raise InvalidAuthorizationCodeError()

    if db_authorization_code.code_challenge_method != 'S256':
        logger.warning("Only S256 code challenge method is supported")
        raise InvalidAuthorizationCodeError()

    computed_challenge = encode_base64(hash_sha256(code_verifier))

    if computed_challenge != db_authorization_code.code_challenge:
        logger.warning("Invalid code Cchallenge")
        raise InvalidAuthorizationCodeError()

    db_user = await crud.get_user_by_id(
        db=db,
        user_id=db_authorization_code.user_id
    )

    if not db_user:
        raise UserNotFoundError()

    db_client = await crud.get_client_by_client_id(
        db=db,
        client_id=client_id
    )

    if not db_client:
        raise ClientNotFoundError()

    access_token = create_jwt(
        expires_in=expire_seconds,
        sub=db_user.username,
        iss='oauth-server',
        aud=db_client.client_id,
        scope=' '.join(db_authorization_code.scopes),
        jti=generate_secret(16)
    )

    return access_token
