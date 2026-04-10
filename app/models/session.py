# coding: utf-8

from datetime import datetime

from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, ForeignKey, Boolean

from app.db import Base
from app.models.base import BaseModelMixin
from app.utils.security import generate_secret


class UserSession(BaseModelMixin, Base):
    __tablename__ = 'oauth_user_sessions'

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('oauth_users.id'),
        nullable=False,
        index=True,
    )

    session_id: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        default=lambda: generate_secret(128),
        nullable=False,
        index=True,
    )

    device_type: Mapped[str] = mapped_column(String(20))
    device_name: Mapped[str] = mapped_column(String(255))

    browser: Mapped[str] = mapped_column(String(100))
    os: Mapped[str] = mapped_column(String(100))

    ip_address: Mapped[str] = mapped_column(String(45))
    user_agent: Mapped[str] = mapped_column(String)

    location: Mapped[str | None] = mapped_column(String(255), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    last_activity: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
