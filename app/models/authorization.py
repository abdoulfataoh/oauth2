# coding: utf-8

from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    ForeignKey,
    TIMESTAMP,
)

from fastapi_oauth2_service.models.base import BaseModelMixin

if TYPE_CHECKING:
    from fastapi_oauth2_service.models.user import User  # noqa: F401


__all__ = [
    'Authorization',
]


class Authorization(BaseModelMixin):
    __tablename__ = 'auth_authorizations'
    user_id = Column(String(64), ForeignKey('auth_users.id'), nullable=False)
    client_id = Column(String(64), ForeignKey('auth_clients.client_id'), nullable=False)
    authorization_code = Column(String(255), nullable=True)
    access_token = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    scope = Column(String(255), nullable=True)
    expires_in = Column(Integer, nullable=True)
    expires_at = Column(TIMESTAMP, nullable=True)
    revoked = Column(Boolean, default=False)
    user = relationship('User', back_populates='authorizations')
