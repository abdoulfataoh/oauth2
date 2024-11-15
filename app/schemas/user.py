# coding: utf-8

from pydantic import BaseModel, ConfigDict
from pydantic import Field, SecretStr, EmailStr

from app.schemas._base import IdMixin, TimestampMixin


__all__ = [
    'UserBase',
    'UserCreate',
    'User',
]


class UserBase(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = Field(min_length=8, max_length=32)


class UserCreate(UserBase):
    password: SecretStr


class User(IdMixin, UserBase, TimestampMixin):
    """
    User in DB representation
    """
    model_config = ConfigDict(from_attributes=True)
    username: str
    disabled: bool | None = None
