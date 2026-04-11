# coding: utf-8

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app import crud
from app import schemas as S
from app import models as M

from app.utils.security import (
    hash_password, verify_password, generate_username,
)

from app.exceptions.domain import (
    UserNotFoundError, UserAlreadyExistsError, AuthenticationFailedError,
    UserDisabledError, InvalidFieldsError,
)


def _validate_contact(email: str | None, phone: str | None) -> None:
    if bool(email) == bool(phone):
        raise InvalidFieldsError("Provide either email or phone, not both at singup")


async def signup(
    db: AsyncSession,
    user: S.UserCreate,
) -> M.User:

    _validate_contact(user.email, user.phone)

    password_hash = hash_password(
        user.password.get_secret_value()
    )

    username = generate_username(
        firstname=user.firstname,
        lastname=user.lastname or 'user',
    )

    try:
        return await crud.create_user(
            db,
            username=username,
            firstname=user.firstname,
            lastname=user.lastname or 'user',
            email=user.email,
            phone=user.phone,
            birthdate=user.birthdate,
            password_hash=password_hash,
            disabled=False,
            verified=False,
            roles=['user'],
        )

    except IntegrityError as e:
        msg = str(e.orig).lower()

        if 'unique' in msg:
            raise UserAlreadyExistsError()

        if 'not null' in msg:
            raise InvalidFieldsError("Missing required field")

        raise


async def create_user(
    db: AsyncSession,
    user: S.UserCreate,
) -> M.User:

    _validate_contact(user.email, user.phone)

    password_hash = hash_password(
        user.password.get_secret_value()
    )

    username = generate_username(
        firstname=user.firstname,
        lastname=user.lastname or 'user',
    )

    try:
        return await crud.create_user(
            db,
            username=username,
            firstname=user.firstname,
            lastname=user.lastname or 'user',
            email=user.email,
            phone=user.phone,
            birthdate=user.birthdate,
            password_hash=password_hash,
            disabled=False,
            verified=True,
            roles=['user'],
        )

    except IntegrityError as e:
        msg = str(e.orig).lower()

        if 'unique' in msg:
            raise UserAlreadyExistsError()

        if 'not null' in msg:
            raise InvalidFieldsError("Missing required field")

        raise


async def update_user_by_id(
    db: AsyncSession,
    user_id: UUID,
    user: S.UserInfoUpdate,
) -> M.User:

    update_data = user.model_dump(exclude_unset=True)

    db_user = await crud.update_user_by_id(
        db,
        user_id,
        update_data,
    )

    if not db_user:
        raise UserNotFoundError()

    return db_user


async def get_user_by_id(
    db: AsyncSession,
    user_id: UUID,
) -> M.User:

    db_user = await crud.get_user_by_id(db, user_id)

    if not db_user:
        raise UserNotFoundError()

    return db_user


async def get_user_by_username(
    db: AsyncSession,
    username: str,
) -> M.User:

    db_user = await crud.get_user_by_username(db, username)

    if not db_user:
        raise UserNotFoundError()

    return db_user


async def silent_get_user_by_contact(
    db: AsyncSession,
    contact: str,
    contact_type: str,
) -> M.User | None:

    if contact_type == 'email':
        db_user = await crud.get_user_by_email(db, email=contact)

    elif contact_type == 'phone':
        db_user = await crud.get_user_by_phone(db, phone=contact)

    return db_user


async def get_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
) -> list[M.User]:

    return list(await crud.get_users(db, skip, limit))


async def delete_user_by_id(
    db: AsyncSession,
    user_id: UUID,
) -> M.User:

    db_user = await crud.delete_user_by_id(db, user_id)

    if not db_user:
        raise UserNotFoundError()

    return db_user


async def update_user_password(
    db: AsyncSession,
    user_id: UUID,
    old_password: str,
    new_password: str,
) -> M.User:

    db_user = await get_user_by_id(
        db,
        user_id=user_id
    )

    if not verify_password(old_password, db_user.password_hash):
        raise AuthenticationFailedError("The current password is incorrect")

    await crud.update_user_password(
        db,
        user_id=user_id,
        password_hash=hash_password(new_password)
    )

    return db_user


async def authenticate_user(
    db: AsyncSession,
    identifier: str,
    password: str,
) -> M.User:
    """
    identifier can be:
    - username
    - email
    - phone
    """

    db_user = await crud.get_user_by_username(db, identifier)

    if not db_user:
        db_user = await crud.get_user_by_email(db, identifier)

    if not db_user:
        db_user = await crud.get_user_by_phone(db, identifier)

    if not db_user:
        raise AuthenticationFailedError()

    if not verify_password(password, db_user.password_hash):
        raise AuthenticationFailedError()

    if db_user.disabled:
        raise UserDisabledError()

    return db_user
