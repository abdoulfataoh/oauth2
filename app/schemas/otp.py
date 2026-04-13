# coding: utf-8

from typing import Literal, Annotated

from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumberValidator

PhoneNumber = Annotated[
    str,
    PhoneNumberValidator(number_format='E164')
]


class Otp(BaseModel):
    otp: str


class NewPassword(BaseModel):
    new_password: str


class OtpRequestEmailChannel(BaseModel):
    channel: Literal['email']
    recipient: EmailStr


class OtpRequestPhoneChannel(BaseModel):
    channel: Literal['phone']
    recipient: PhoneNumber


class OtpCheckEmailChannel(OtpRequestEmailChannel, Otp):
    pass


class OtpCheckPhoneChannel(OtpRequestPhoneChannel, Otp):
    pass


class ResetPasswordEmail(OtpCheckEmailChannel, NewPassword):
    pass


class ResetPasswordPhone(OtpCheckPhoneChannel, NewPassword):
    pass


OtpRequest = Annotated[
    OtpRequestEmailChannel | OtpRequestPhoneChannel,
    Field(discriminator='channel')
]

OtpCheck = Annotated[
    OtpCheckEmailChannel | OtpCheckPhoneChannel,
    Field(discriminator='channel')
]

ResetPassword = Annotated[
    ResetPasswordEmail | ResetPasswordPhone,
    Field(discriminator='channel')
]
