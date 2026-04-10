# coding: utf-8

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


__all__ = ['BaseORM']


class BaseORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    edited_at: datetime | None = None
