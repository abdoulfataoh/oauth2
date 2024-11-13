# coding: utf-8


from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    Boolean,
)

from app.models.base import BaseModelMixin

if TYPE_CHECKING:
    from app.models.authorization import Authorization  # noqa: F401


__all__ = [
    'User',
]


class User(BaseModelMixin):
    __tablename__ = 'auth_users'
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    full_name = Column(String(128), nullable=True)
    phone_number = Column(String(32), unique=True, nullable=True)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=False)
    authorizations = relationship('Authorization', back_populates='user')
