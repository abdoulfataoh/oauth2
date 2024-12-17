# coding: utf-8

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas as S
from app.utils.security import decode_jwt
from app import crud as CRUD
from app.db import get_db
from app.utils.exceptions import (
    UserNotFoundException,
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/oauth2/token')


async def check_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db)
) -> S.User | None:
    """
    Decode user data by token
    """
    payload = decode_jwt(token)
    user_id = payload['sub']
    db_user = await CRUD.get_user(db=db, user_id=user_id)
    if not db_user:
        UserNotFoundException
    user_model = S.User.model_validate(db_user)
    return user_model
