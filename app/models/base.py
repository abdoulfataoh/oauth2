# coding: utf-8

from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.utils.datetime import utcnow


class BaseModelMixin:
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
    )

    edited_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow,
    )
