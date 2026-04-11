# coding: utf-8

from uuid import UUID
from urllib.parse import urlencode
from typing import Optional

from fastapi import APIRouter, Depends, Request, Query, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import models as M
from app import settings
from app.db import get_db
from app.utils.devices import parse_device

from app import services

from app.security.dependencies import (
    get_current_user_from_cookie,
    get_optional_user_from_cookie,
)

from app.exceptions.domain import (
    AuthenticationFailedError, UserDisabledError,
    UnsupportedResponseTypeError, InvalidScopeError,
    InvalidCodeChallengeMethodError, InvalidCodeChallengeError,
    ClientAuthenticationFailedError, InvalidClientRedirectURIError,
)

router = APIRouter()


@router.post('/login')
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    request_id: Optional[UUID] = Form(None),
    next: Optional[str] = Form(''),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse:

    try:
        db_user = await services.authenticate_user(
            identifier=username,
            password=password,
            db=db,
        )

    except (AuthenticationFailedError, UserDisabledError):

        params: dict[str, str] = {
            'error': 'invalid_credentials',
        }

        if request_id:
            params['request_id'] = str(request_id)

        return RedirectResponse(
            f'{settings.OAUTH_UI_LOGIN_URL}?{urlencode(params)}',
            status_code=302,
        )

    user_agent = request.headers.get('user-agent', '')
    user_device = parse_device(user_agent)
    ip_address = request.client.host if request.client else ''

    session = await services.create_session(
        db=db,
        user=db_user,
        user_agent=user_agent,
        ip_address=ip_address,
        device_type=user_device['device_type'],
        device_name=user_device['device_name'],
        browser=user_device['browser'],
        os=user_device['os'],
        location=None,
    )

    if request_id:

        await services.attach_user_to_request(
            request_id=request_id,
            user_id=db_user.id,
            db=db,
        )

        redirect = f'{settings.OAUTH_UI_CONSENT_URL}?request_id={request_id}'

    else:

        if next:
            redirect = f'{settings.OAUTH_UI_URI}{next}'
        else:
            redirect = settings.OAUTH_USER_ACCOUNT_URL

    ui_access_token = session.session_id

    response = RedirectResponse(
        redirect,
        status_code=302,
    )

    response.set_cookie(
        key='ui_access_token',
        value=ui_access_token,
        httponly=True,
        secure=settings.UI_ACCESS_COOKIES_ONLY_ON_HTTPS,
        samesite='lax',
        max_age=settings.UI_ACCESS_COOKIES_EXPIRE_MINUTES,
    )

    return response


@router.get('/authorize')
async def authorize(
    client_id: str,
    redirect_uri: str,
    state: str,
    code_challenge: str,
    code_challenge_method: str = 'S256',
    scope: list[str] = Query(...),
    response_type: str = 'code',
    user: M.User | None = Depends(get_optional_user_from_cookie),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse:

    try:
        db_request = await services.request_authorize(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scopes=scope,
            response_type=response_type,
            state=state,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
            db=db,
        )

    except (
        UnsupportedResponseTypeError,
        InvalidScopeError,
        InvalidCodeChallengeMethodError,
        InvalidCodeChallengeError,
        ClientAuthenticationFailedError,
        InvalidClientRedirectURIError,
    ):

        params = {
            'error': 'invalid_request',
            'state': state,
        }

        return RedirectResponse(
            f'{redirect_uri}?{urlencode(params)}',
            status_code=302,
        )

    if not user:

        params = {
            'request_id': str(db_request.id),
        }

        return RedirectResponse(
            f'{settings.OAUTH_UI_LOGIN_URL}?{urlencode(params)}',
            status_code=302,
        )

    await services.attach_user_to_request(
        db=db,
        request_id=db_request.id,
        user_id=user.id,
    )

    params = {
        'request_id': str(db_request.id),
    }

    return RedirectResponse(
        f'{settings.OAUTH_UI_CONSENT_URL}?{urlencode(params)}',
        status_code=302,
    )


@router.post('/consent')
async def consent(
    request_id: UUID = Form(...),
    approved: bool = Form(...),
    user: M.User = Depends(get_current_user_from_cookie),
    db: AsyncSession = Depends(get_db),
):

    db_request = await services.get_authorization_request_by_id(
        db=db,
        request_id=request_id,
    )

    if not approved:

        params = {
            'error': 'access_denied',
            'error_description': 'The user denied the request',
            'state': db_request.state,
        }

    else:

        db_code = await services.approve_consent(
            request_id=request_id,
            user_id=user.id,
            approved=True,
            db_request=db_request,
            db=db,
        )

        params = {
            'code': db_code.code,
            'state': db_request.state,
        }

    redirect_uri = f'{db_request.redirect_uri}?{urlencode(params)}'

    return RedirectResponse(
        redirect_uri,
        status_code=302,
    )


@router.post('/token')
async def token():
    return {
        'detail': 'Not implemented yet',
    }
