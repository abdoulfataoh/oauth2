# coding: utf-8

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON

from app.db import Base
from app.models.base import BaseModelMixin


class Client(BaseModelMixin, Base):
    __tablename__ = 'oauth_clients'

    client_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    client_secret: Mapped[str] = mapped_column(String, nullable=False)
    redirect_uri: Mapped[str] = mapped_column(String(2048), unique=True, nullable=False)
    client_name: Mapped[str | None] = mapped_column(String, nullable=False, default='')
    allowed_scopes: Mapped[list[str]] = mapped_column(JSON)
