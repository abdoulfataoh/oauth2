# coding: utf-8

from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, JSON, Date, CheckConstraint

from app.db import Base
from app.models.base import BaseModelMixin


class User(BaseModelMixin, Base):
    __tablename__ = 'oauth_users'

    __table_args__ = (
        CheckConstraint(
            'email IS NOT NULL OR phone IS NOT NULL',
            name='ck_user_email_or_phone',
        ),
    )

    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    email: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), unique=True, nullable=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    firstname: Mapped[str] = mapped_column(String(128), nullable=False, default='')
    lastname: Mapped[str] = mapped_column(String(128), nullable=False, default='')

    birthdate: Mapped[date | None] = mapped_column(Date, nullable=True)

    roles: Mapped[list[str]] = mapped_column(JSON, default=list)

    disabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    password_hash: Mapped[str] = mapped_column(String, nullable=False)
