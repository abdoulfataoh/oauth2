# coding: utf-8

from uuid import uuid4
from datetime import datetime
import secrets

from pydantic import BaseModel, ConfigDict
from pydantic import Field, SecretStr

from fastapi_oauth2_service.schemas.base import IdMixin


__all__ = [
    'ClientBase',
    'ClientCreate',
    'Client',
]


class ClientBase(BaseModel):
    client_id: str = Field(default_factory=lambda: str(uuid4()))
    redirect_uri: str
    client_name: str


class ClientCreate(ClientBase):
    client_secret: SecretStr = Field(default_factory=lambda: secrets.token_urlsafe(16))


class Client(IdMixin, ClientBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime = Field(default_factory=datetime.now)
    edited_at: datetime | None = None
