# coding: utf-8

from uuid import uuid4

from pydantic import BaseModel, ConfigDict
from pydantic import Field, SecretStr

from app.schemas._base import IdMixin, TimestampMixin


__all__ = [
    'ClientBase',
    'ClientCreate',
    'Client',
]


class ClientBase(BaseModel):
    client_id: str = Field(default_factory=lambda: str(uuid4()))
    client_secret: SecretStr


class ClientCreate(BaseModel):
    redirect_uri: str
    client_name: str


class Client(IdMixin, ClientBase, ClientCreate, TimestampMixin):
    """
    Client in DB representation
    """
    model_config = ConfigDict(from_attributes=True)
