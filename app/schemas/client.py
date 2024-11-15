# coding: utf-8

from pydantic import BaseModel, ConfigDict
from pydantic import SecretStr

from app.schemas._base import IdMixin, TimestampMixin


__all__ = [
    'ClientBase',
    'ClientCreate',
    'Client',
]


class ClientBase(BaseModel):
    client_secret: SecretStr


class ClientCreate(BaseModel):
    redirect_uri: str
    client_name: str


class Client(IdMixin, ClientCreate, TimestampMixin):
    """
    Client in DB representation
    """
    model_config = ConfigDict(from_attributes=True)
    client_id: str
