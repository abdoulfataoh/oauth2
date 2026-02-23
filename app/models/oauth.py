# coding: utf-8

from sqlalchemy import String, ForeignKey, Boolean, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db import Base
from app.models.base import BaseModelMixin


class OAuthAuthorizationRequest(BaseModelMixin, Base):
    __tablename__ = 'oauth_authorization_requests'

    client_id: Mapped[str] = mapped_column(
        ForeignKey('oauth_clients.id', ondelete='CASCADE'),
        nullable=False
    )

    redirect_uri: Mapped[str] = mapped_column(String(2048), nullable=False)
    scopes: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    state: Mapped[str] = mapped_column(String(256), nullable=False)
    code_challenge: Mapped[str] = mapped_column(String(256), nullable=False)
    code_challenge_method: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default='S256'
    )

    user_id: Mapped[str | None] = mapped_column(
        ForeignKey('oauth_users.id', ondelete='SET NULL'),
        nullable=True
    )

    approved: Mapped[bool | None] = mapped_column(
        Boolean,
        default=None
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    client = relationship('Client')


class OAuthAuthorizationCode(BaseModelMixin, Base):
    __tablename__ = 'oauth_authorization_codes'

    code: Mapped[str] = mapped_column(
        String(128),
        primary_key=True
    )

    client_id: Mapped[str] = mapped_column(
        ForeignKey('oauth_clients.id', ondelete='CASCADE'),
        nullable=False
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey('oauth_users.id', ondelete='CASCADE'),
        nullable=False
    )

    redirect_uri: Mapped[str] = mapped_column(
        String(2048),
        nullable=False
    )

    scopes: Mapped[list[str]] = mapped_column(JSON, nullable=False)

    code_challenge: Mapped[str] = mapped_column(
        String(256),
        nullable=False
    )

    code_challenge_method: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    used: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    client = relationship('Client')
