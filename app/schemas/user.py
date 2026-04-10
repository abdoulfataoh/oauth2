# coding: utf-8

from datetime import date

from pydantic import BaseModel, ConfigDict
from pydantic import Field, SecretStr, EmailStr, model_validator

from app.schemas.base import BaseORM


class UserCommon(BaseModel):

    email: EmailStr | None = None
    phone: str | None = Field(
        default=None,
        min_length=8,
        max_length=32
    )

    @model_validator(mode='after')
    def validate_contact(self):
        if not self.email and not self.phone:
            raise ValueError('email or phone required')
        return self


class UserBase(BaseModel):
    firstname: str
    lastname: str
    birthdate: date | None = None


class UserCreate(UserBase, UserCommon):
    password: SecretStr


class UserInfoUpdate(UserBase):
    pass


class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str


class UserEmailUpdate(BaseModel):
    email: EmailStr


class User(BaseORM, UserBase, UserCommon):
    model_config = ConfigDict(from_attributes=True)

    username: str
    roles: list[str] | str = 'user'
    verified: bool
    disabled: bool
