# coding: utf-8

from uuid import uuid4
from datetime import datetime
import pytz

from sqlalchemy import (
    Column,
    String,
    DateTime,
)

from app.db import Base


__all__ = [
    'Base',
]


class BaseModelMixin(Base):
    __abstract__ = True
    id = Column(String(64), primary_key=True, default=lambda: str(uuid4()))
    created_at = Column(DateTime, default=lambda x: datetime.now(tz=pytz.utc))
    edited_at = Column(DateTime, onupdate=lambda x: datetime.now(tz=pytz.utc))
