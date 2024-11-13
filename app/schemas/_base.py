# coding: utf-8

from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field


__all__ = [
    'IdMixin'
]


class IdMixin(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
