# coding: utf-8

from typing import Literal, Union
from pydantic import BaseModel, EmailStr


class Channel(BaseModel):
    channel: Literal['email', 'phone']


class Otp(BaseModel):
    otp: str


class NewPassword(BaseModel):
    new_password: str


class OtpRequestEmailChannel(Channel):
    recipient: EmailStr


class OtpRequestPhoneChannel(Channel):
    recipient: str


class OtpCheckEmailChannel(OtpRequestEmailChannel, Otp):
    pass


class OtpCheckPhoneChannel(OtpRequestPhoneChannel, Otp):
    pass


OtpRequest = Union[OtpRequestEmailChannel, OtpRequestPhoneChannel]
OtpCheck = Union[OtpCheckEmailChannel, OtpCheckPhoneChannel]


class ResetPassword(Channel, Otp, NewPassword):
    recipient: str
