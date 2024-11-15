# coding: utf-8

from datetime import timedelta
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Form, Depends, Response
# from fastapi.responses import RedirectResponse

from app.utils.exceptions import LoginFailedException
from app import crud as CRUD
from app.db import get_db


__all__ = [
    'router',
]


router = APIRouter()


@router.post('/oauth2/login/')
async def login(
    username: Annotated[str, Form()], password: Annotated[str, Form()],
    response: Response, db: AsyncSession = Depends(get_db),
):
    # Auth user
    db_user = await CRUD.authenticate_user(
        db=db, username=username, password=password
    )
    if not db_user:
        raise LoginFailedException

    # Write session
    db_session = await CRUD.create_session(db=db, username=username)
    if not db_session:
        raise LoginFailedException

    # Set cookie
    session_id = db_session.session_id
    response.set_cookie(key='session_id', value=session_id, max_age=timedelta(minutes=30))
    return {'message': f'Welcone {username}'}
