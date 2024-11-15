# coding: utf-8

from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic import Field, SecretStr, EmailStr

from app.schemas._base import IdMixin


__all__ = [
    'UserBase',
    'UserCreate',
    'User',
]


class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None
    phone_number: str | None = Field(min_length=8, max_length=32)
    firstname: str | None = None
    lastname: str | None = None
    disabled: bool | None = None


class UserCreate(UserBase):
    password: SecretStr


class User(IdMixin, UserBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime = Field(default_factory=datetime.now)
    edited_at: datetime | None = None
