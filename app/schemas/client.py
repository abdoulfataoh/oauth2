# coding: utf-8

from uuid import uuid4
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic import Field, SecretStr

from app.schemas._base import IdMixin


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
    client_secret: SecretStr


class Client(IdMixin, ClientBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime = Field(default_factory=datetime.now)
    edited_at: datetime | None = None
