# coding: utf-8

from enum import Enum


class OtpTypeEnum(Enum):
    SIGNUP = 'signup'
    CHANGE_PASSWORD = 'change_password'
    CHANGE_EMAIL = 'change_email'
    CHANGE_PHONE = 'change_phone'
