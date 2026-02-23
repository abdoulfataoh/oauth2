# coding: utf-8

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, JSON

from app.db import Base
from app.models.base import BaseModelMixin


class User(BaseModelMixin, Base):
    __tablename__ = 'oauth_users'

    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String, unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(128), nullable=False, default='')
    lastname: Mapped[str] = mapped_column(String(128), nullable=False, default='')
    phone: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, default='')
    roles: Mapped[list[str]] = mapped_column(JSON, default=[])
    disabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
