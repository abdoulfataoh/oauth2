# coding: utf-8

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from app.schemas._base import IdMixin


__all__ = [
    'AuthorizationCreate',
    'AuthorizationUpdate',
    'Authorization',
]


class AuthorizationCreate(BaseModel):
    user_id: str
    client_id: str
    authorization_code: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    expires_in: Optional[int] = None
    expires_at: Optional[datetime] = None
    revoked: Optional[bool] = Field(default=False)


class AuthorizationUpdate(BaseModel):
    authorization_code: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    expires_in: Optional[int] = None
    expires_at: Optional[datetime] = None
    revoked: Optional[bool] = None


class Authorization(IdMixin, BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    client_id: str
    authorization_code: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    expires_in: Optional[int] = None
    expires_at: Optional[datetime] = None
    revoked: bool
