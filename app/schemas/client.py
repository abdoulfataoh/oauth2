# coding: utf-8

from pydantic import BaseModel, ConfigDict
from pydantic import SecretStr

from app.schemas.base import BaseORM


class ClientBase(BaseModel):
    client_name: str
    redirect_uri: str
    allowed_scopes: list[str]


class ClientCreate(ClientBase):
    pass


class ClientRead(BaseORM, ClientBase):
    client_id: str
    model_config = ConfigDict(from_attributes=True)


class ClientDB(BaseORM, ClientBase):
    """
    Client DB representation
    """
    client_id: str
    client_secret: SecretStr
    model_config = ConfigDict(from_attributes=True)
