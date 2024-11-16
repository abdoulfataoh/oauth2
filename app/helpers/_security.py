# coding: utf-8

from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas as S
from app.utils.security import decode_jwt
from app import crud as CRUD
from app.db import get_db
from app.utils.exceptions import UserNotFoundException


async def _check_user(request: Request, db: AsyncSession = Depends(get_db)) -> S.User | None:
    access_token = request.cookies.get('access_token')
    if not access_token:
        """
        NotTokenFound, redirect ?
        """
    payload = decode_jwt(access_token)
    print(payload)
    user_id = payload['sub']
    db_user = await CRUD.get_user(db=db, user_id=user_id)
    if not db_user:
        UserNotFoundException
    user_data = S.User.model_validate(db_user)
    return user_data
