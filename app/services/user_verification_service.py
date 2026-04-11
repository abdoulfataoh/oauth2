# coding: utf-8

from uuid import UUID
from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import models as M
from app.utils.security import generate_otp
from app.utils.datetime import utcnow, is_expired
from app.utils.security import hash_password
from app.exceptions.domain import (
    OtpExpiredError,
    TooManyVerificationAttemptsError,
    InvalidOtpError,
    InvalidResetPasswordError,
    UserNotFoundError,
    DomainException,
)


def resolve_otp_recipient(user):
    channel = 'email' if user.email else ('sms' if user.phone else None)
    recipient = user.email or user.phone
    return channel, recipient


async def send_otp(
    db: AsyncSession,
    *,
    user_id: UUID,
    recipient: str,
    otp_type: str,
    channel: str,
    expire_seconds: int
) -> str:

    code = generate_otp()
    expires_at = utcnow() + timedelta(seconds=expire_seconds)

    existing_otp = await crud.get_otp(
        db,
        user_id=user_id,
        recipient=recipient,
        otp_type=otp_type,
        channel=channel,
    )

    if existing_otp:
        await crud.delete_otp(db, existing_otp.id)

    await crud.create_otp(
        db,
        user_id=user_id,
        recipient=recipient,
        channel=channel,
        code=code,
        otp_type=otp_type,
        expires_at=expires_at,
    )

    print('\n\n\n\n\n\n\n')
    print('*****************************')
    print('***********', code, '********')
    print('***********', otp_type, '********')
    print('***********', channel, '********')
    print('***********', recipient, '********')
    print('*****************************')
    print('\n\n\n\n\n\n\n')

    return code


async def _validate_otp(
    db: AsyncSession,
    *,
    user_id: UUID,
    recipient: str,
    otp_type: str,
    channel: str,
    code: str,
    max_attempts: int,
    consume: bool = True

) -> M.Otp:

    db_otp = await crud.get_otp(
        db,
        user_id=user_id,
        recipient=recipient,
        otp_type=otp_type,
        channel=channel,
    )

    if not db_otp:
        raise InvalidOtpError("Invalid OTP")

    if is_expired(db_otp.expires_at):
        raise OtpExpiredError("OTP expired")

    if db_otp.attempts >= max_attempts:
        raise TooManyVerificationAttemptsError("Too many attempts")

    if db_otp.code != code:
        await crud.increment_otp_attempts(db, otp_id=db_otp.id)
        raise InvalidOtpError("Invalid OTP")

    if consume:
        await crud.delete_otp(db, otp_id=db_otp.id)

    return db_otp


async def validate_otp_without_consume(
    db: AsyncSession,
    *,
    user_id: UUID | None,
    recipient: str,
    otp_type: str,
    channel: str,
    code: str,
    max_attempts: int
) -> M.Otp:

    if not user_id:
        raise InvalidOtpError("Invalid OTP")

    db_otp = await _validate_otp(
        db,
        user_id=user_id,
        recipient=recipient,
        otp_type=otp_type,
        channel=channel,
        code=code,
        max_attempts=max_attempts,
        consume=False,
    )

    if not db_otp:
        raise InvalidOtpError("Invalid OTP")

    return db_otp


async def validate_signup(
    db: AsyncSession,
    user_id: UUID,
    channel: str,
    recipient: str,
    code: str,
    max_attempts: int,
) -> M.User:

    await _validate_otp(
        db,
        user_id=user_id,
        recipient=recipient,
        otp_type='signup',
        channel=channel,
        code=code,
        max_attempts=max_attempts,
        consume=True,
    )

    db_user = await crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise UserNotFoundError()

    db_user.verified = True

    await db.commit()
    await db.refresh(db_user)

    return db_user


async def validate_contact_change(
    db: AsyncSession,
    user_id: UUID,
    recipient: str,
    channel: str,
    code: str,
    max_attempts: int,
) -> M.User:

    db_otp = await _validate_otp(
        db,
        user_id=user_id,
        recipient=recipient,
        otp_type=f'change_{channel}',
        channel=channel,
        code=code,
        max_attempts=max_attempts,
        consume=True,
    )

    db_user = await crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise UserNotFoundError()

    new_contact = db_otp.recipient
    setattr(db_user, channel, new_contact)

    await db.commit()
    await db.refresh(db_user)

    return db_user


async def validate_password_change(
    db: AsyncSession,
    user_id: UUID | None,
    recipient: str,
    channel: str,
    code: str,
    new_password: str,
    max_attempts: int,
) -> M.User:

    try:
        if not user_id:
            raise UserNotFoundError()

        db_otp = await _validate_otp(
            db,
            user_id=user_id,
            recipient=recipient,
            otp_type='change_password',
            channel=channel,
            code=code,
            max_attempts=max_attempts,
            consume=True,
        )

        if not db_otp.user_id:
            raise UserNotFoundError()

        db_user = await crud.get_user_by_id(db, db_otp.user_id)
        if not db_user:
            raise UserNotFoundError()

        db_user.password_hash = hash_password(new_password)

        await db.commit()
        await db.refresh(db_user)

    except DomainException:
        raise InvalidResetPasswordError()

    return db_user
