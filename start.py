# coding: utf-8

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.endpoints import health, auth, user, client
from app.utils.exceptions_handlers import validation_exception_handler


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(health.router, tags=['Monitoring'])

app.include_router(auth.router, tags=['Auth'])

app.include_router(user.router, tags=['User'])

app.include_router(client.router, tags=['Client Application'])
