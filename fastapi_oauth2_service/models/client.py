# coding: utf-8

from sqlalchemy import Column, String

from fastapi_oauth2_service.models.base import BaseModelMixin


class Client(BaseModelMixin):
    __tablename__ = 'auth_clients'
    client_id = Column(String(64), unique=True, nullable=False)
    client_secret = Column(String, nullable=False)
    redirect_uri = Column(String(2048), unique=True, nullable=False)
    client_name = Column(String, nullable=True)
