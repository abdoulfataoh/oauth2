# coding: utf-8

from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)

from app.db import Base
from app.models.base import BaseModelMixin


class Otp(BaseModelMixin, Base):
    __tablename__ = 'oauth_otp'

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('oauth_users.id'),
        nullable=True,
    )

    recipient: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        index=True,
    )

    otp_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    channel: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    __table_args__ = (
        UniqueConstraint(
            'recipient',
            'otp_type',
            name='uq_otp_recipient_otp_type',
        ),
    )
