# coding: utf-8

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from app import settings
from app import schemas as S
from app import models as M
from app.models import OtpTypeEnum
from app.db import get_db
from app.security.dependencies import CurrentUser
from app.security.permissions import AdminUser, ReadUserToken
from app.utils.devices import parse_device
from app import services

router = APIRouter()
DB = Annotated[AsyncSession, Depends(get_db)]


def to_user_schema(user: M.User) -> S.User:
    return S.User.model_validate(user)


def to_user_list(users: list[M.User]) -> list[S.User]:
    return [S.User.model_validate(u) for u in users]


# AUTH
@router.post('/signup', response_model=S.User, status_code=201)
async def signup(
    request: Request,
    user: S.UserCreate,
    response: Response,
    db: DB,
) -> S.User:

    db_user = await services.signup(db, user)

    channel, recipient = services.resolve_otp_recipient(user)

    await services.send_otp(
        db,
        user_id=db_user.id,
        recipient=recipient,
        channel=channel,
        expire_seconds=settings.OTP_EXPIRE_SECOND,
        otp_type=OtpTypeEnum.SIGNUP,
    )

    user_agent = request.headers.get('user-agent', '')
    user_device = parse_device(user_agent)

    ip_address = request.headers.get(
        'x-forwarded-for', request.client.host if request.client else ''
    )

    session = await services.create_session(
        db=db,
        user_id=db_user.id,
        user_agent=user_agent,
        ip_address=ip_address,
        device_type=user_device['device_type'],
        device_name=user_device['device_name'],
        browser=user_device['browser'],
        os=user_device['os'],
        location=None,
    )

    response.set_cookie(
        key='ui_access_token',
        value=session.session_id,
        httponly=True,
        secure=settings.UI_COOKIES_ONLY_ON_HTTPS,
        samesite='lax',
        max_age=settings.UI_COOKIES_EXPIRE_SECONDS,
    )

    return to_user_schema(db_user)


@router.post('/password/request', status_code=204)
async def request_reset_password(
    payload: S.OtpRequest,
    db: DB,
) -> None:

    db_user = await services.silent_get_user_by_contact(
        db, contact=payload.recipient, contact_type=payload.channel
    )

    if db_user:
        await services.send_otp(
            db,
            user_id=db_user.id,
            recipient=payload.recipient,
            channel=payload.channel,
            expire_seconds=settings.OTP_EXPIRE_SECOND,
            otp_type=OtpTypeEnum.CHANGE_PASSWORD,
        )


@router.post('/password/verify', status_code=200)
async def verify_reset_password(
    payload: S.OtpCheck,
    db: DB,
):
    db_user = await services.silent_get_user_by_contact(
        db,
        contact=payload.recipient,
        contact_type=payload.channel,
    )

    user_id = db_user.id if db_user else None

    await services.validate_otp_without_consume(
        db,
        user_id=user_id,
        recipient=payload.recipient,
        channel=payload.channel,
        code=payload.otp,
        otp_type=OtpTypeEnum.CHANGE_PASSWORD,
        max_attempts=settings.OTP_MAX_ATTEMPTS,
    )


@router.post('/password/reset', response_model=S.User)
async def reset_password(
    payload: S.ResetPassword,
    db: DB,
):

    db_user = await services.silent_get_user_by_contact(
        db,
        contact=payload.recipient,
        contact_type=payload.channel,
    )

    user_id = db_user.id if db_user else None

    db_user = await services.validate_password_change(
        db,
        user_id=user_id,
        recipient=payload.recipient,
        channel=payload.channel,
        code=payload.otp,
        new_password=payload.new_password,
        max_attempts=settings.OTP_MAX_ATTEMPTS,
    )

    return to_user_schema(db_user)


@router.put('/users/me/password', response_model=S.User)
async def update_me_password(
    db: DB, current_user: CurrentUser, password: S.UserPasswordUpdate
) -> S.User:

    db_user = await services.update_user_password(
        db,
        user_id=current_user.id,
        old_password=password.old_password,
        new_password=password.new_password,
    )

    return to_user_schema(db_user)


# CURRENT USER
@router.get('/users/me', response_model=S.User)
async def me(current_user: CurrentUser) -> S.User:
    return to_user_schema(current_user)


# Client
@router.get('/users/userinfo', response_model=S.User)
async def userinfo(user: ReadUserToken, db: DB) -> S.User:
    return to_user_schema(user)


@router.put('/users/me', response_model=S.User)
async def update_me(
    payload: S.UserInfoUpdate,
    db: DB,
    current_user: CurrentUser,
) -> S.User:

    db_user = await services.update_user_by_id(
        db,
        current_user.id,
        payload,
    )

    return to_user_schema(db_user)


@router.post('/users/me/verification/resend', status_code=204)
async def resend_signup_otp(
    db: DB,
    current_user: CurrentUser,
) -> None:

    channel, recipient = services.resolve_otp_recipient(current_user)

    await services.send_otp(
        db,
        user_id=current_user.id,
        recipient=recipient,
        channel=channel,
        otp_type=OtpTypeEnum.SIGNUP,
        expire_seconds=settings.OTP_EXPIRE_SECOND,
    )


@router.post('/users/me/verification/verify', response_model=S.User)
async def verify_signup(
    payload: S.OtpCheck,
    db: DB,
    current_user: CurrentUser,
) -> S.User:

    db_user = await services.validate_signup(
        db,
        user_id=current_user.id,
        channel=payload.channel,
        recipient=payload.recipient,
        code=payload.otp,
        max_attempts=settings.OTP_MAX_ATTEMPTS,
    )

    return to_user_schema(db_user)


# CONTACT
@router.post('/users/me/contact/request', status_code=204)
async def request_contact_change(
    payload: S.OtpRequest, db: DB, current_user: CurrentUser
) -> None:

    otp_type = OtpTypeEnum(f'change_{payload.channel}')

    await services.send_otp(
        db,
        user_id=current_user.id,
        recipient=payload.recipient,
        otp_type=otp_type,
        channel=payload.channel,
        expire_seconds=settings.OTP_EXPIRE_SECOND,
    )


@router.post('/users/me/contact/verify', response_model=S.User)
async def verify_contact_change(
    payload: S.OtpCheck,
    db: DB,
    current_user: CurrentUser,
) -> S.User:

    db_user = await services.validate_contact_change(
        db,
        user_id=current_user.id,
        recipient=payload.recipient,
        channel=payload.channel,
        code=payload.otp,
        max_attempts=settings.OTP_MAX_ATTEMPTS,
    )

    return to_user_schema(db_user)


# SESSIONS
@router.get('/users/me/sessions', response_model=list[S.UserSession])
async def get_my_sessions(
    request: Request,
    current_user: CurrentUser,
    db: DB,
) -> list[S.UserSession]:

    token = request.cookies.get('ui_access_token')
    db_sessions = await services.get_my_sessions(db, user_id=current_user.id)

    sessions = [S.UserSession.model_validate(session) for session in db_sessions]

    for s, session in zip(sessions, db_sessions):
        if token == session.session_id:
            s.is_current = True

    return sessions


@router.post('/users/me/sessions/logout')
async def logout(request: Request, db: DB):

    token = request.cookies.get('ui_access_token')

    if token:
        await services.logout_session(
            db=db,
            session_id=token,
        )

    response = JSONResponse({'success': True})
    response.delete_cookie('ui_access_token')
    return response


# ADMIN USERS
@router.post('/users', response_model=S.User, status_code=201)
async def add_user(user: S.UserCreate, db: DB, current_user: AdminUser) -> S.User:
    db_user = await services.create_user(db, user)
    return to_user_schema(db_user)


@router.get('/users', response_model=list[S.User])
async def get_users(db: DB, current_user: AdminUser) -> list[S.User]:
    db_users = await services.get_users(db)
    return to_user_list(db_users)


@router.get('/users/{user_id}', response_model=S.User)
async def get_user_by_id(user_id: UUID, db: DB, current_user: AdminUser) -> S.User:
    db_user = await services.get_user_by_id(db, user_id)
    return to_user_schema(db_user)


@router.put('/users/{user_id}', response_model=S.User)
async def update_user_by_id(
    user_id: UUID,
    user: S.UserInfoUpdate,
    db: DB,
    current_user: AdminUser,
) -> S.User:
    db_user = await services.update_user_by_id(db, user_id, user)
    return to_user_schema(db_user)


@router.delete('/users/{user_id}', response_model=S.User)
async def delete_user(user_id: UUID, db: DB, current_user: AdminUser) -> S.User:
    db_user = await services.delete_user_by_id(db, user_id)
    return to_user_schema(db_user)
