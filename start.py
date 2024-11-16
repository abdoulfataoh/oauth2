# coding: utf-8

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.endpoints import health, auth, user, client
from app.utils.exceptions_handlers import validation_exception_handler


app = FastAPI()

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(health.router, tags=['Monitoring'])

app.include_router(auth.router, tags=['Auth'])

app.include_router(user.router, tags=['User'])

app.include_router(client.router, tags=['Client Application'])
