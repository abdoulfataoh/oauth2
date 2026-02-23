# coding: utf-8

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String
from uuid import uuid4
from datetime import datetime

from app.utils.datetime import utcnow


class BaseModelMixin:
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True,
        default=lambda: str(uuid4())
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow
    )

    edited_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=utcnow,
        default=utcnow
    )
