# coding: utf-8

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.routes import health, oauth, user, client
from app.exceptions.handlers import register_exception_handlers

from app import settings


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.OAUTH_UI_URI],
    allow_credentials=True,
    allow_headers=['*'],
    allow_methods=[
        'GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD', 'PATCH'
    ]
)

register_exception_handlers(app)

api_router = APIRouter(prefix=settings.OAUTH_API_PREFIX)

api_router.include_router(health.router, tags=['Monitoring'])
api_router.include_router(oauth.router, tags=['Auth'])
api_router.include_router(user.router, tags=['User'])
api_router.include_router(client.router, tags=['Client apps'])

app.include_router(api_router)
