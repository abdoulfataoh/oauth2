# coding: utf-8

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from app import crud
from app import schemas as S
from app import models as M
from app.utils.security import (
    hash_password,
    verify_password,
    generate_username,
)
from app.utils.exceptions import (
    UserNotFoundException, ConflictedUserException,
    LoginFailedException, InvalidFieldsException
)


async def create_user_service(
    db: AsyncSession,
    user: S.UserCreate,
) -> M.User:
    password_hash = hash_password(user.password.get_secret_value())

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
            password_hash=password_hash,
            disabled=False,
            roles=['user']
        )
    except IntegrityError as e:
        msg = str(e.orig).lower()

        if 'unique' in msg:
            raise ConflictedUserException()
        if 'not null' in msg:
            raise InvalidFieldsException("Missing required field")
        raise


async def update_user_by_id_service(
    db: AsyncSession,
    user_id: str,
    user: S.UserInfoUpdate,
) -> M.User:
    update_data = user.model_dump(exclude_unset=True)

    db_user = await crud.update_user_by_id(
        db,
        user_id,
        update_data,
    )

    if not db_user:
        raise UserNotFoundException

    return db_user


async def get_user_by_id_service(
    db: AsyncSession,
    user_id: str,
) -> M.User:
    db_user = await crud.get_user_by_id(db, user_id)

    if not db_user:
        raise UserNotFoundException

    return db_user


async def get_user_by_username_service(
    db: AsyncSession,
    username: str,
) -> M.User:
    db_user = await crud.get_user_by_username(db, username)

    if not db_user:
        raise UserNotFoundException

    return db_user


async def get_users_service(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
) -> list[M.User]:
    return list(await crud.get_users(db, skip, limit))


async def delete_user_by_id_service(
    db: AsyncSession,
    user_id: str,
) -> M.User:
    db_user = await crud.delete_user_by_id(db, user_id)

    if not db_user:
        raise UserNotFoundException

    return db_user


async def authenticate_user_service(
    db: AsyncSession,
    username: str,
    password: str,
) -> M.User:
    db_user = await crud.get_user_by_username(db, username)

    if not db_user:
        raise LoginFailedException

    if not verify_password(password, db_user.password_hash):
        raise LoginFailedException

    if db_user.disabled:
        raise LoginFailedException("User disabled")

    return db_user
