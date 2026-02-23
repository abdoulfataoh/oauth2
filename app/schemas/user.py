# coding: utf-8

from pydantic import BaseModel, ConfigDict
from pydantic import Field, SecretStr, EmailStr

from app.schemas.base import BaseORM


class UserCommon(BaseModel):
    email: EmailStr
    phone: str | None = Field(min_length=8, max_length=32)


class UserBase(BaseModel):
    firstname: str
    lastname: str | None = None


class UserCreate(UserBase, UserCommon):
    password: SecretStr


class UserInfoUpdate(UserBase):
    pass


class UserEmailUpdate(BaseModel):
    email: EmailStr


class User(BaseORM, UserBase, UserCommon):
    """
    User in DB representation
    """
    model_config = ConfigDict(from_attributes=True)
    username: str
    roles: list[str] | str = 'user'
    disabled: bool | None = None
