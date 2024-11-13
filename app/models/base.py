# coding: utf-8

from uuid import uuid4

from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    String,
    DateTime,
)

from fastapi_oauth2_service.db import Base


__all__ = [
    'Base',
]


class BaseModelMixin(Base):
    __abstract__ = True
    id = Column(String(64), primary_key=True, default=lambda: str(uuid4()))
    created_at = Column(DateTime, server_default=func.now())
    edited_at = Column(DateTime, onupdate=func.now())
