# coding: utf-8

from datetime import datetime

from pydantic import BaseModel, ConfigDict


__all__ = ['BaseORM']


class BaseORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    edited_at: datetime | None = None
