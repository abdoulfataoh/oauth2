# coding: utf-8

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    Boolean,
)

from fastapi_oauth2_service.models.base import BaseModelMixin


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
