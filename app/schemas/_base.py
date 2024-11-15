# coding: utf-8

from uuid import uuid4
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


__all__ = [
    'IdMixin'
]


class IdMixin(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))


class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    edited_at: datetime | None = None
