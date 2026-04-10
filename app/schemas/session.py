# coding: utf-8

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserSession(BaseModel):
    id: UUID

    device_type: str
    device_name: str

    browser: str
    os: str

    ip_address: str
    location: str | None

    is_active: bool

    last_activity: datetime

    is_current: bool = False

    model_config = ConfigDict(from_attributes=True)
