# coding: utf-8

from fastapi import FastAPI

from fastapi_oauth2_service.api import router


app = FastAPI()
app.include_router(router, tags=['Authentification'])
