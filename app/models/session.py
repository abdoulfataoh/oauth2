# coding: utf-8

from sqlalchemy import (
    Column,
    String,
    DateTime,
)
from sqlalchemy.sql import func

from app.models.base import Base


__all__ = [
    'Session',
]


class Session(Base):
    __tablename__ = "auth_sessions"
    session_id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True)
    last_access = Column(DateTime, default=func.now())
    expires_at = Column(DateTime)
